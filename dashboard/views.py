from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from sermons.models import Sermon
from events.models import Event
from ministry.models import PrayerRequest, ContactSubmission, Testimony
from .models import SiteSettings
from .forms import SermonForm, EventForm, SiteSettingsForm

from .forms import SermonForm, EventForm, SiteSettingsForm

def staff_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='dashboard:login'
    )(view_func)
    return decorated_view_func

# --- Authentication ---

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:home')
    else:
        form = AuthenticationForm()
    return render(request, 'dashboard/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('dashboard:login')

# --- Main Dashboard ---

@staff_required
def dashboard_home(request):
    context = {
        'total_sermons': Sermon.objects.count(),
        'upcoming_events': Event.objects.filter(is_completed=False).count(),
        'prayer_requests': PrayerRequest.objects.filter(is_prayed_for=False).count(),
    }
    return render(request, 'dashboard/home.html', context)

# --- Sermon Management ---

@staff_required
def sermon_list(request):
    sermons = Sermon.objects.all().order_by('-date_preached')
    return render(request, 'dashboard/sermon_list.html', {'sermons': sermons})

@staff_required
def sermon_create(request):
    if request.method == 'POST':
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:sermon_list')
    else:
        form = SermonForm()
    return render(request, 'dashboard/sermon_form.html', {'form': form})

@staff_required
def sermon_edit(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)
    if request.method == 'POST':
        form = SermonForm(request.POST, request.FILES, instance=sermon)
        if form.is_valid():
            form.save()
            return redirect('dashboard:sermon_list')
    else:
        form = SermonForm(instance=sermon)
    return render(request, 'dashboard/sermon_form.html', {'form': form})

# --- Event Management ---

@staff_required
def event_list(request):
    events = Event.objects.all().order_by('start_time')
    return render(request, 'dashboard/event_list.html', {'events': events})

@staff_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:event_list')
    else:
        form = EventForm()
    return render(request, 'dashboard/event_form.html', {'form': form})

@staff_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard:event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'dashboard/event_form.html', {'form': form})

# --- Ministry Management ---

@staff_required
def prayer_list(request):
    # Order: not prayed for first, then by date (newest first)
    requests = PrayerRequest.objects.all().order_by('is_prayed_for', '-created_at')
    return render(request, 'dashboard/prayer_list.html', {'requests': requests})

@staff_required
def mark_prayed(request, pk):
    req = get_object_or_404(PrayerRequest, pk=pk)
    req.is_prayed_for = not req.is_prayed_for
    req.save()
    return redirect('dashboard:prayer_list')

@staff_required
def mark_followed_up(request, pk):
    from django.utils import timezone
    req = get_object_or_404(PrayerRequest, pk=pk)
    req.is_followed_up = not req.is_followed_up
    req.followed_up_at = timezone.now() if req.is_followed_up else None
    req.save()
    return redirect('dashboard:prayer_list')

@staff_required
@staff_required
def contact_list(request):
    submissions = ContactSubmission.objects.all().order_by('-created_at')
    return render(request, 'dashboard/contact_list.html', {'submissions': submissions})

@staff_required
def testimony_list(request):
    testimonies = Testimony.objects.all().order_by('-created_at')
    return render(request, 'dashboard/testimony_list.html', {'testimonies': testimonies})

@staff_required
def testimony_detail(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    return render(request, 'dashboard/testimony_detail.html', {'testimony': testimony})

@staff_required
def approve_testimony(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    # Toggle logic: if approved, unapprove; if pending, approve.
    # But for clarity in UI, let's keep it as toggle.
    testimony.is_approved = not testimony.is_approved
    testimony.save()
    # Redirect back to where they came from if possible, or list
    return redirect('dashboard:testimony_detail', pk=pk) # Better UX to stay on detail if that's where we were

@staff_required
def delete_testimony(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    if request.method == 'POST':
        testimony.delete()
    return redirect('dashboard:testimony_list')

# --- Settings & Configuration ---

@staff_required
def settings_view(request):
    settings_obj = SiteSettings.load()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard:settings')
    else:
        form = SiteSettingsForm(instance=settings_obj)
    return render(request, 'dashboard/settings.html', {'form': form})

@staff_required
def content_settings_view(request):
    settings_obj = SiteSettings.load()
    from .forms import ContentSettingsForm # Import inside to avoid circular if any
    if request.method == 'POST':
        form = ContentSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard:content_settings')
    else:
        form = ContentSettingsForm(instance=settings_obj)
    return render(request, 'dashboard/content_settings.html', {'form': form})

@staff_required
def giving_history(request):
    # Placeholder for giving history; expand when Payment Gateway is active
    return render(request, 'dashboard/giving_history.html')

# --- User Management ---

@staff_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})

# --- Communications: Follow-ups ---

@staff_required
def followup_list(request):
    """List all prayer requests that have requested follow-up."""
    requests = PrayerRequest.objects.filter(request_followup=True).order_by('-created_at')
    pending_count = requests.filter(is_followed_up=False).count()
    return render(request, 'dashboard/followup_list.html', {
        'requests': requests,
        'pending_count': pending_count
    })

@staff_required
def followup_compose(request, pk):
    """Compose and send a follow-up email."""
    from django.contrib import messages
    from .email_service import get_default_followup_template, send_followup_email
    from django.utils import timezone
    
    prayer_request = get_object_or_404(PrayerRequest, pk=pk)
    
    # Get default template
    name = prayer_request.name or "Friend"
    default_template = get_default_followup_template(name)
    
    if request.method == 'POST':
        subject = request.POST.get('subject', default_template['subject'])
        message = request.POST.get('message', '')
        
        if not prayer_request.email:
            messages.error(request, "This request has no email address to send to.")
            return redirect('dashboard:followup_list')
        
        # Send the email
        result = send_followup_email(
            to_email=prayer_request.email,
            to_name=name,
            subject=subject,
            html_content=message
        )
        
        if result['success']:
            # Mark as followed up
            prayer_request.is_followed_up = True
            prayer_request.followed_up_at = timezone.now()
            prayer_request.save()
            messages.success(request, f"Email sent successfully to {prayer_request.email}")
        else:
            messages.error(request, result.get('error', 'Failed to send email'))
        
        return redirect('dashboard:followup_list')
    
    return render(request, 'dashboard/followup_compose.html', {
        'prayer_request': prayer_request,
        'default_subject': default_template['subject'],
        'default_message': default_template['message']
    })

# --- Communications: Newsletters ---

@staff_required
def newsletter_list(request):
    """Newsletter dashboard showing subscriber count."""
    from core.models import NewsletterSubscriber
    
    subscribers = NewsletterSubscriber.objects.all().order_by('-created_at')
    return render(request, 'dashboard/newsletter_list.html', {
        'subscribers': subscribers,
        'subscriber_count': subscribers.count()
    })

@staff_required
def newsletter_compose(request):
    """Compose and send newsletter to all subscribers."""
    from django.contrib import messages
    from core.models import NewsletterSubscriber
    from .email_service import send_newsletter
    
    subscribers = NewsletterSubscriber.objects.all()
    
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        content = request.POST.get('content', '')
        
        if not subject or not content:
            messages.error(request, "Please provide both subject and content.")
            return render(request, 'dashboard/newsletter_compose.html', {
                'subscriber_count': subscribers.count(),
                'subject': subject,
                'content': content
            })
        
        # Build subscriber list
        subscriber_list = [{'email': s.email, 'name': ''} for s in subscribers]
        
        # Send newsletter
        result = send_newsletter(
            subject=subject,
            html_content=content,
            subscribers=subscriber_list
        )
        
        if result['success']:
            messages.success(request, f"Newsletter sent to {result['sent_count']} subscribers!")
        else:
            messages.error(request, result.get('error', 'Failed to send newsletter'))
        
        return redirect('dashboard:newsletter_list')
    
    return render(request, 'dashboard/newsletter_compose.html', {
        'subscriber_count': subscribers.count()
    })


# --- Counsel Sessions (Dashboard) ---

@staff_required
def counsel_sessions(request):
    """Dashboard view for managing counsel sessions."""
    from counsel.models import Conversation
    
    # Get unassigned (waiting) conversations
    waiting = Conversation.objects.filter(
        counsellor__isnull=True,
        is_active=True
    ).select_related('user').order_by('-created_at')
    
    # Get active conversations for this counsellor
    active = Conversation.objects.filter(
        counsellor=request.user,
        is_active=True
    ).select_related('user').order_by('-updated_at')
    
    # Get completed/closed conversations
    closed = Conversation.objects.filter(
        counsellor=request.user,
        is_active=False
    ).select_related('user').order_by('-updated_at')[:20]
    
    return render(request, 'dashboard/counsel_sessions.html', {
        'waiting': waiting,
        'active': active,
        'closed': closed,
        'waiting_count': waiting.count(),
        'active_count': active.count(),
    })


@staff_required
def counsel_chat(request, conversation_id):
    """Dashboard chat view for a specific conversation."""
    from counsel.models import Conversation, Message
    
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Assign counsellor if not assigned
    if conversation.counsellor is None:
        conversation.counsellor = request.user
        conversation.save()
    
    # Get messages
    chat_messages = conversation.messages.all().order_by('timestamp')
    
    return render(request, 'dashboard/counsel_chat.html', {
        'conversation': conversation,
        'chat_messages': chat_messages,
    })


@staff_required
def counsel_close(request, conversation_id):
    """Close a conversation."""
    from counsel.models import Conversation
    from django.contrib import messages as django_messages
    
    conversation = get_object_or_404(Conversation, id=conversation_id)
    conversation.is_active = False
    conversation.save()
    
    django_messages.success(request, "Conversation closed.")
    return redirect('dashboard:counsel_sessions')
