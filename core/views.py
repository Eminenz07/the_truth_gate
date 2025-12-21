from django.shortcuts import render, get_object_or_404
from .models import Category, Sermon

def home(request):
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'categories': categories})

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
