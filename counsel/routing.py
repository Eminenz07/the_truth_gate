"""
WebSocket URL routing for counselling chat.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/counsel/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
