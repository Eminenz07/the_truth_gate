"""
Views for counselling chat system.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Conversation, Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@login_required
def counsel_home(request):
    """Main counsel page for regular users - shows their conversations."""
    user = request.user
    
    # Regular users see their own conversations
    conversations = Conversation.objects.filter(
        user=user, 
        is_active=True,
        user_deleted=False
    ).select_related('counsellor').order_by('-updated_at')
    
    return render(request, 'counsel/counsel_home.html', {
        'conversations': conversations,
    })


@login_required
def start_conversation(request):
    """Start a new counselling conversation."""
    # Check for existing active conversation
    active_conversation = Conversation.objects.filter(user=request.user, is_active=True).first()
    if active_conversation:
        messages.info(request, "You already have an active session.")
        return redirect('counsel:chat', conversation_id=active_conversation.id)

    if request.method == 'POST':
        retention = request.POST.get('retention', 'permanent')
        
        # Create new conversation
        conversation = Conversation.objects.create(
            user=request.user,
            retention_mode=retention,
        )
        
        messages.success(request, "Your counselling session has been started. A counsellor will join shortly.")
        return redirect('counsel:chat', conversation_id=conversation.id)
    
    return render(request, 'counsel/start_conversation.html')


@login_required
def chat_room(request, conversation_id):
    """Chat room for a specific conversation."""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    user = request.user
    
    # Check access
    if not (conversation.user == user or user.is_staff):
        messages.error(request, "You don't have access to this conversation.")
        return redirect('counsel:home')
    
    # If staff is accessing, assign them as counsellor if not assigned
    if user.is_staff and conversation.counsellor is None:
        conversation.counsellor = user
        conversation.save()
    
    # Get messages (exclude deleted)
    chat_messages = conversation.messages.filter(is_deleted=False).order_by('timestamp')
    
    return render(request, 'counsel/chat_room.html', {
        'conversation': conversation,
        'chat_messages': chat_messages,
        'is_counsellor': user.is_staff,
    })


@login_required
def delete_conversation(request, conversation_id):
    """Soft-delete conversation from user's view."""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    if conversation.user != request.user:
        messages.error(request, "You can only delete your own conversations.")
        return redirect('counsel:home')
    
    conversation.user_deleted = True
    conversation.save()
    messages.success(request, "Conversation removed from your history.")
    return redirect('counsel:home')


@login_required
def edit_message(request, message_id):
    """Edit a message (AJAX endpoint)."""
    import json
    from django.utils import timezone
    from django.views.decorators.http import require_POST
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)
    
    message = get_object_or_404(Message, id=message_id)
    
    # Only sender can edit their own message
    if message.sender != request.user:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        new_content = data.get('content', '').strip()
        
        if not new_content:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty'}, status=400)
        
        message.content = new_content
        message.edited_at = timezone.now()
        message.save()
        
        # Broadcast edit to room group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'counsel_{message.conversation.id}',
            {
                'type': 'chat_message_edit',
                'message_id': message.id,
                'content': message.content,
                'edited_at': message.edited_at.isoformat()
            }
        )
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'content': message.content,
            'edited_at': message.edited_at.isoformat()
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)


@login_required
def delete_message(request, message_id):
    """Soft-delete a message (AJAX endpoint)."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)
    
    message = get_object_or_404(Message, id=message_id)
    
    # Only sender can delete their own message
    if message.sender != request.user:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    conversation_id = message.conversation.id
    message.is_deleted = True
    message.save()
    
    # Broadcast delete to room group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'counsel_{conversation_id}',
        {
            'type': 'chat_message_delete',
            'message_id': message.id,
        }
    )
    
    return JsonResponse({
        'success': True,
        'message_id': message.id
    })


def get_online_status(request):
    """API endpoint to check if any counsellor is online."""
    from django.contrib.auth.models import User
    
    # For now, check if any staff member has been active recently
    # In production, this would use presence detection
    online = User.objects.filter(is_staff=True, is_active=True).exists()
    
    return JsonResponse({'online': online})


@login_required
def widget_messages(request):
    """API endpoint for floating widget to fetch recent messages."""
    user = request.user
    
    # Get user's active conversation
    active_conversation = Conversation.objects.filter(
        user=user,
        is_active=True,
        user_deleted=False
    ).select_related('counsellor').first()
    
    if not active_conversation:
        return JsonResponse({'error': 'No active conversation'}, status=404)
    
    # Get recent messages (last 60, excluding deleted)
    messages = active_conversation.messages.filter(
        is_deleted=False
    ).order_by('-timestamp')[:60]
    
    # Reverse to show oldest first
    messages = list(reversed(messages))
    
    # Mark unread messages from other users (counsellors) as read
    unread_messages = [msg for msg in messages if not msg.is_read and msg.sender != user]
    if unread_messages:
        for msg in unread_messages:
            msg.is_read = True
        Message.objects.bulk_update(unread_messages, ['is_read'])
    
    # Format messages for JSON response
    messages_data = [{
        'id': msg.id,
        'content': msg.content,
        'sender_id': msg.sender.id,
        'sender_name': msg.sender.get_full_name() or msg.sender.username,
        'timestamp': msg.timestamp.isoformat(),
        'edited_at': msg.edited_at.isoformat() if msg.edited_at else None
    } for msg in messages]
    
    return JsonResponse({
        'conversation_id': active_conversation.id,
        'messages': messages_data,
        'counsellor_name': active_conversation.counsellor.get_full_name() if active_conversation.counsellor else 'Counsellor'
    })


