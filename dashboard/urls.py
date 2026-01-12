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
    path('prayer/<int:pk>/followup/', views.mark_followed_up, name='mark_followed_up'),
    path('inbox/', views.contact_list, name='contact_list'),
    
    path('testimony/', views.testimony_list, name='testimony_list'),
    path('testimony/<int:pk>/', views.testimony_detail, name='testimony_detail'),
    path('testimony/<int:pk>/approve/', views.approve_testimony, name='approve_testimony'),
    path('testimony/<int:pk>/delete/', views.delete_testimony, name='delete_testimony'),
    
    path('users/', views.user_list, name='user_list'),
    
    path('content/', views.content_settings_view, name='content_settings'),
    path('settings/', views.settings_view, name='settings'),
    path('giving/', views.giving_history, name='giving_history'),
    
    # Communications
    path('followups/', views.followup_list, name='followup_list'),
    path('followups/<int:pk>/compose/', views.followup_compose, name='followup_compose'),
    path('newsletters/', views.newsletter_list, name='newsletter_list'),
    path('newsletters/compose/', views.newsletter_compose, name='newsletter_compose'),
]
