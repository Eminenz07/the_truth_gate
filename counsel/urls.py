from django.urls import path
from . import views

app_name = 'counsel'

urlpatterns = [
    path('', views.counsel_home, name='home'),
    path('start/', views.start_conversation, name='start'),
    path('chat/<int:conversation_id>/', views.chat_room, name='chat'),
    path('delete/<int:conversation_id>/', views.delete_conversation, name='delete'),
    path('api/status/', views.get_online_status, name='online_status'),
    path('api/message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('api/message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
]
