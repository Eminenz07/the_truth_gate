from django.urls import path
from . import views

urlpatterns = [
    path('prayer/', views.prayer_request_view, name='prayer_request'),
    path('contact/', views.contact_view, name='contact'),
    path('testimony/share/', views.submit_testimony, name='submit_testimony'),
    path('testimony/', views.testimony_list, name='testimony_list'),
    path('testimony/<int:pk>/', views.testimony_detail, name='testimony_detail'),
]
