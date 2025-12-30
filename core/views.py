from django.shortcuts import render, get_object_or_404
from .models import Category
from sermons.models import Sermon, Topic
from ministry.models import Testimony

from dashboard.models import SiteSettings

def home(request):
    # Use Topics as Categories for the filter tabs
    categories = Topic.objects.all()
    # Fetch latest 3 approved testimonies
    testimonies = Testimony.objects.filter(is_approved=True).order_by('-created_at')[:3]
    # Fetch recent sermons (V2)
    recent_sermons = Sermon.objects.all().order_by('-date_preached')[:10]
    # Fetch Site Settings for Live Banner
    settings = SiteSettings.load()
    
    return render(request, 'core/home.html', {
        'categories': categories, 
        'testimonies': testimonies,
        'recent_sermons': recent_sermons,
        'settings': settings
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
