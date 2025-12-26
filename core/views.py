from django.shortcuts import render, get_object_or_404
from .models import Category, Sermon
from ministry.models import Testimony

def home(request):
    categories = Category.objects.all()
    # Fetch latest 3 approved testimonies
    testimonies = Testimony.objects.filter(is_approved=True).order_by('-created_at')[:3]
    # Fetch recent sermons for "Browse by Topic"
    recent_sermons = Sermon.objects.all().order_by('-date')[:10]
    return render(request, 'core/home.html', {
        'categories': categories, 
        'testimonies': testimonies,
        'recent_sermons': recent_sermons
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
