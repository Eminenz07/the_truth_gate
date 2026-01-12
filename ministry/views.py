from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from .models import Testimony, PrayerRequest, ContactSubmission, Donation
import secrets
import requests
import json
import logging
import hmac
import hashlib

import bleach

logger = logging.getLogger(__name__)

# --- Existing Views ---

@login_required
def submit_testimony(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        content = request.POST.get('content')
        
        # Sanitize HTML
        clean_content = bleach.clean(content, tags=['b', 'i', 'p', 'br', 'strong', 'em'], strip=True)
        
        Testimony.objects.create(name=name, location=location, content=clean_content)
        messages.success(request, "Your testimony has been submitted for review. Thank you for sharing!")
        # Redirect to the testimony submission page to show the success message in context
        return redirect('testimony_list') 
    
    return render(request, 'ministry/submit_testimony.html')

def testimony_list(request):
    testimonies = Testimony.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'ministry/testimony_list.html', {'testimonies': testimonies})

def testimony_detail(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk, is_approved=True)
    return render(request, 'ministry/testimony_detail.html', {'testimony': testimony})

def prayer_request(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        request_text = request.POST.get('request_text')
        request_followup = request.POST.get('request_followup') == 'on'
        
        # If they want follow-up but aren't logged in, ignore follow-up request
        if request_followup and not request.user.is_authenticated:
            request_followup = False
        
        # Use logged-in user's email if authenticated, otherwise empty
        email = request.user.email if request.user.is_authenticated else ''
        
        PrayerRequest.objects.create(
            name=name, email=email, request_text=request_text, request_followup=request_followup
        )
        messages.success(request, "Your prayer request has been received. We are standing with you in prayer.")
        return redirect('home')
        
    return render(request, 'ministry/prayer_request.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactSubmission.objects.create(
            name=name, email=email, subject=subject, message=message
        )
        messages.success(request, "Thank you for contacting us. We will get back to you shortly.")
        return redirect('home')
        
    return render(request, 'ministry/contact.html')


# --- Paystack Payment Logic ---

def initiate_donation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        amount = request.POST.get('amount') # In Naira (e.g. 5000)

        if not email or not amount:
            messages.error(request, "Please provide both an email and an amount.")
            return redirect('give')

        try:
            amount_decimal = float(amount)
            if amount_decimal < 100: # Minimum 100 Naira
                 messages.error(request, "Minimum donation amount is N100.")
                 return redirect('give')
        except ValueError:
            messages.error(request, "Invalid amount.")
            return redirect('give')

        # Generate unique internal reference
        ref = secrets.token_urlsafe(16)
        
        # Create Pending Donation
        donation = Donation.objects.create(
            email=email,
            amount=amount_decimal,
            reference=ref,
            status='PENDING'
        )

        # Initialize Paystack Transaction
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": email,
            "amount": int(amount_decimal * 100), # Paystack expects Kobo
            "reference": ref,
            "callback_url": request.build_absolute_uri('/give/verify/'), # Fallback callback
        }

        try:
            response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
            response_data = response.json()

            if response_data['status']:
                # Save Paystack reference if needed (often same as ours if we sent it)
                # Redirect user to Paystack
                return redirect(response_data['data']['authorization_url'])
            else:
                logger.error(f"Paystack Init Failed: {response_data}")
                messages.error(request, "Could not initialize payment. Please try again.")
                return redirect('give')

        except Exception as e:
            logger.error(f"Paystack Error: {e}")
            messages.error(request, "Connection error. Please try again later.")
            return redirect('give')

    return render(request, 'ministry/give.html')


@csrf_exempt
@require_POST
def paystack_webhook(request):
    """
    Secure Webhook to verify transactions server-side.
    """
    paystack_signature = request.headers.get('x-paystack-signature')
    
    if not paystack_signature:
        return HttpResponseBadRequest("Missing signature")

    # Verify Signature
    body = request.body
    # Ensure PAYSTACK_SECRET_KEY is bytes for hmac
    secret = settings.PAYSTACK_SECRET_KEY.encode('utf-8')
    computed_sig = hmac.new(secret, body, hashlib.sha512).hexdigest()

    if computed_sig != paystack_signature:
        logger.warning("Paystack Webhook Signature Verification Failed")
        return HttpResponseBadRequest("Invalid signature")

    # Process Event
    try:
        payload = json.loads(body)
        event = payload.get('event')
        data = payload.get('data', {})

        if event == 'charge.success':
            reference = data.get('reference')
            
            # Find Donation
            try:
                donation = Donation.objects.get(reference=reference)
            except Donation.DoesNotExist:
                logger.error(f"Webhook received for unknown reference: {reference}")
                return HttpResponse(status=200) # Ack to stop retries even if not found

            # 1. Idempotency Check (Prevent duplicate processing)
            if donation.status == 'SUCCESS':
                logger.info(f"Duplicate webhook received for already successful donation: {reference}")
                return HttpResponse(status=200)

            # Double Verify via API (Defense in Depth)
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
            v_response = requests.get(verify_url, headers=headers)
            v_data = v_response.json()

            if v_data['status'] and v_data['data']['status'] == 'success':
                 # 2. Strict Amount & Currency Verification
                 paid_amount_kobo = v_data['data']['amount'] # Paystack returns Kobo (Integer)
                 paid_currency = v_data['data']['currency']
                 
                 # Convert our stored Decimal Naira to Kobo Integer for comparison
                 expected_amount_kobo = int(donation.amount * 100)

                 if paid_currency != 'NGN':
                     logger.error(f"Invalid Currency for {reference}: Expected NGN, Got {paid_currency}")
                     donation.status = 'FAILED'
                     donation.save()
                     return HttpResponse(status=200)

                 if paid_amount_kobo != expected_amount_kobo:
                     logger.critical(f"FRAUD ATTEMPT: Amount Mismatch for {reference}. Expected {expected_amount_kobo}, Paid {paid_amount_kobo}")
                     donation.status = 'FAILED' # Or 'FRAUD_SUSPECTED'
                     donation.save()
                     return HttpResponse(status=200) # Ack Paystack to stop retrying, but don't give value.

                 # All Checks Passed
                 donation.status = 'SUCCESS'
                 donation.verified = True
                 donation.paystack_ref = str(data.get('id')) # Store Paystack ID
                 donation.save()
                 logger.info(f"Donation {reference} verified successfully.")
            else:
                 logger.warning(f"Donation {reference} verification failed via API check.")
                 donation.status = 'FAILED'
                 donation.save()
        
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        logger.error(f"Webhook Processing Error: {e}")
        return HttpResponse(status=500)

    return HttpResponse(status=200)

def donation_success(request):
    return render(request, 'ministry/give_success.html')

def verify_callback(request):
    """
    Optional client-side return URL handler.
    Ideally, we just show 'Processing...' or check status via AJAX.
    """
    ref = request.GET.get('reference')
    # We could check DB status here, but the webhook is the source of truth.
    # For now, just show the success page or a 'Check Status' page.
    return render(request, 'ministry/give_success.html')
