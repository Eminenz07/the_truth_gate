from django.urls import path
from . import views

urlpatterns = [
    path('submit-testimony/', views.submit_testimony, name='submit_testimony'),
    path('testimonies/', views.testimony_list, name='testimony_list'),
    path('testimonies/<int:pk>/', views.testimony_detail, name='testimony_detail'),
    path('prayer-request/', views.prayer_request, name='prayer_request'),
    path('contact/', views.contact, name='contact'),
    
    # Paystack Donation URLs
    path('webhooks/paystack/', views.paystack_webhook, name='paystack_webhook'),
]
