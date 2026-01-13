"""
Views for counselling chat system.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Conversation, Message


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
    
    # Get messages
    chat_messages = conversation.messages.all().order_by('timestamp')
    
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


def get_online_status(request):
    """API endpoint to check if any counsellor is online."""
    from django.contrib.auth.models import User
    
    # For now, check if any staff member has been active recently
    # In production, this would use presence detection
    online = User.objects.filter(is_staff=True, is_active=True).exists()
    
    return JsonResponse({'online': online})
