from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('give/', views.give, name='give'),
    path('secure-access/<str:token>/', views.authorize_device, name='authorize_device'),
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:sermon_slug>/', views.sermon_detail, name='sermon_detail'),
]
