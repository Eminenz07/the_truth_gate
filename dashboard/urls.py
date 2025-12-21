from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('', views.dashboard_home, name='home'),
    path('sermons/', views.sermon_list, name='sermon_list'),
    path('sermons/add/', views.sermon_create, name='sermon_create'),
    path('sermons/<int:pk>/edit/', views.sermon_edit, name='sermon_edit'),
    
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    
    path('prayer/', views.prayer_list, name='prayer_list'),
    path('prayer/<int:pk>/mark/', views.mark_prayed, name='mark_prayed'),
    path('inbox/', views.contact_list, name='contact_list'),
    
    path('settings/', views.settings_view, name='settings'),
    path('giving/', views.giving_history, name='giving_history'),
]
