from django.urls import path
from . import views

urlpatterns = [
    path('prayer/', views.prayer_request_view, name='prayer_request'),
    path('contact/', views.contact_view, name='contact'),
    path('testimony/share/', views.submit_testimony, name='submit_testimony'),
]
