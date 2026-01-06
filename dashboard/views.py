from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from sermons.models import Sermon
from events.models import Event
from ministry.models import PrayerRequest, ContactSubmission, Testimony
from .models import SiteSettings
from .forms import SermonForm, EventForm, SiteSettingsForm

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

@staff_member_required
def dashboard_home(request):
    context = {
        'total_sermons': Sermon.objects.count(),
        'upcoming_events': Event.objects.filter(is_completed=False).count(),
        'prayer_requests': PrayerRequest.objects.filter(is_prayed_for=False).count(),
    }
    return render(request, 'dashboard/home.html', context)

# --- Sermon Management ---

@staff_member_required
def sermon_list(request):
    sermons = Sermon.objects.all().order_by('-date_preached')
    return render(request, 'dashboard/sermon_list.html', {'sermons': sermons})

@staff_member_required
def sermon_create(request):
    if request.method == 'POST':
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:sermon_list')
    else:
        form = SermonForm()
    return render(request, 'dashboard/sermon_form.html', {'form': form})

@staff_member_required
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

@staff_member_required
def event_list(request):
    events = Event.objects.all().order_by('start_time')
    return render(request, 'dashboard/event_list.html', {'events': events})

@staff_member_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:event_list')
    else:
        form = EventForm()
    return render(request, 'dashboard/event_form.html', {'form': form})

@staff_member_required
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

@staff_member_required
def prayer_list(request):
    requests = PrayerRequest.objects.all().order_by('-created_at')
    return render(request, 'dashboard/prayer_list.html', {'requests': requests})

@staff_member_required
def mark_prayed(request, pk):
    req = get_object_or_404(PrayerRequest, pk=pk)
    req.is_prayed_for = not req.is_prayed_for
    req.save()
    return redirect('dashboard:prayer_list')

@staff_member_required
@staff_member_required
def contact_list(request):
    submissions = ContactSubmission.objects.all().order_by('-created_at')
    return render(request, 'dashboard/contact_list.html', {'submissions': submissions})

@staff_member_required
def testimony_list(request):
    testimonies = Testimony.objects.all().order_by('-created_at')
    return render(request, 'dashboard/testimony_list.html', {'testimonies': testimonies})

@staff_member_required
def testimony_detail(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    return render(request, 'dashboard/testimony_detail.html', {'testimony': testimony})

@staff_member_required
def approve_testimony(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    # Toggle logic: if approved, unapprove; if pending, approve.
    # But for clarity in UI, let's keep it as toggle.
    testimony.is_approved = not testimony.is_approved
    testimony.save()
    # Redirect back to where they came from if possible, or list
    return redirect('dashboard:testimony_detail', pk=pk) # Better UX to stay on detail if that's where we were

@staff_member_required
def delete_testimony(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    if request.method == 'POST':
        testimony.delete()
    return redirect('dashboard:testimony_list')

# --- Settings & Configuration ---

@staff_member_required
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

@staff_member_required
def giving_history(request):
    # Placeholder for giving history; expand when Payment Gateway is active
    return render(request, 'dashboard/giving_history.html')

# --- User Management ---

@staff_member_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})
