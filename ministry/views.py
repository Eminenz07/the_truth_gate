from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PrayerRequest, ContactSubmission, Testimony

def testimony_detail(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk, is_approved=True)
    return render(request, 'ministry/testimony_detail.html', {'testimony': testimony})

def submit_testimony(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        location = request.POST.get('location', '')
        content = request.POST.get('content')
        
        if content:
            Testimony.objects.create(
                name=name,
                location=location,
                content=content,
                is_approved=False # Default
            )
            messages.success(request, "Your testimony has been submitted for review. Thank you for sharing!")
            return redirect('home') # Or wherever
        else:
             messages.error(request, "Please share your story.")
             
    return render(request, 'ministry/submit_testimony.html')

def prayer_request_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        request_text = request.POST.get('request_text')
        is_private = request.POST.get('is_private') == 'on'

        PrayerRequest.objects.create(
            name=name,
            email=email,
            request_text=request_text,
            is_private=is_private
        )
        messages.success(request, "Your prayer request has been received.")
        return redirect('prayer_request')

    return render(request, 'ministry/prayer_request.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactSubmission.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Thank you for contacting us. We will get back to you soon.")
        return redirect('contact')

    return render(request, 'ministry/contact.html')
