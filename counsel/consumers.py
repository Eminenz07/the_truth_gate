"""
WebSocket consumer for counselling chat.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time counselling chat.
    Handles message sending/receiving between users and counsellors.
    """
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'counsel_{self.conversation_id}'
        
        # Check if user is authenticated
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close()
            return
        
        # Verify user has access to this conversation
        has_access = await self.check_conversation_access(user)
        if not has_access:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            return
        
        try:
            data = json.loads(text_data)
            message_content = data.get('message', '').strip()
            
            if not message_content:
                return
            
            # Save message to database
            message = await self.save_message(user, message_content)
            
            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'sender_id': user.id,
                    'sender_username': user.username,
                    'timestamp': message.timestamp.isoformat(),
                    'message_id': message.id,
                }
            )
        except json.JSONDecodeError:
            pass
    
    async def chat_message(self, event):
        """Send message to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
        }))
    
    @database_sync_to_async
    def check_conversation_access(self, user):
        """Check if user has access to this conversation."""
        from .models import Conversation
        
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            # User owns the conversation OR is staff (counsellor)
            return conversation.user == user or user.is_staff
        except Conversation.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, user, content):
        """Save message to database."""
        from .models import Conversation, Message
        
        conversation = Conversation.objects.get(id=self.conversation_id)
        message = Message.objects.create(
            conversation=conversation,
            sender=user,
            content=content
        )
        # Update conversation timestamp
        conversation.save()  # Triggers auto_now on updated_at
        return message
