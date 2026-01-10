from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import Http404, HttpResponse
from .models import Category
from sermons.models import Sermon, Topic
from ministry.models import Testimony

from dashboard.models import SiteSettings

def authorize_device(request, token):
    if token == settings.DEVICE_AUTH_TOKEN:
        response = redirect('dashboard:login')
        # Set a long-lived cookie (1 year)
        max_age = 365 * 24 * 60 * 60
        response.set_cookie(
            settings.TRUSTED_COOKIE_NAME,
            'true',
            max_age=max_age,
            httponly=True,
            secure=not settings.DEBUG,  # True in production (HTTPS)
            samesite='Lax'
        )
        return response
    else:
        # Invalid token, return 404 to hide endpoint
        raise Http404()

def home(request):
    # Use Topics as Categories for the filter tabs
    categories = Topic.objects.all()
    # Fetch latest 3 approved testimonies
    testimonies = Testimony.objects.filter(is_approved=True).order_by('-created_at')[:3]
    # Fetch recent sermons (V2)
    recent_sermons = Sermon.objects.all().order_by('-date_preached')[:10]
    # Fetch Site Settings for Live Banner
    site_config = SiteSettings.load()
    
    return render(request, 'core/home.html', {
        'categories': categories, 
        'testimonies': testimonies,
        'recent_sermons': recent_sermons,
        'site_config': site_config
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    sermons = category.sermons.all()
    return render(request, 'core/category_detail.html', {'category': category, 'sermons': sermons})

def sermon_detail(request, category_slug, sermon_slug):
    sermon = get_object_or_404(Sermon, category__slug=category_slug, slug=sermon_slug)
    return render(request, 'core/sermon_detail.html', {'sermon': sermon})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def give(request):
    return render(request, 'core/give.html')

def watch_live(request):
    return render(request, 'core/watch_live.html')
