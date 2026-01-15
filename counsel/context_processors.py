from django.db.models import Q
from .models import Conversation, Message

def counsel_notifications(request):
    """
    Context processor to provide notification counts for counsel sessions.
    """
    if not request.user.is_authenticated:
        return {}

    counts = {
        'counsel_badge_count': 0,
        'user_unread_count': 0,
        'has_active_session': False
    }

    user = request.user

    # Logic for Admin/Staff (Counsellors)
    if user.is_staff:
        # 1. Unread messages in conversations where this user is the counsellor
        # OR unassigned conversations (if we want admins to see them)
        
        # Unread messages in assigned conversations
        unread_assigned = Message.objects.filter(
            conversation__counsellor=user,
            is_read=False,
            is_deleted=False
        ).exclude(sender=user).count()
        
        # Active sessions that are unassigned (waiting for a counsellor)
        unassigned_sessions = Conversation.objects.filter(
            counsellor__isnull=True,
            is_active=True,
            user_deleted=False
        ).count()
        
        counts['counsel_badge_count'] = unread_assigned + unassigned_sessions

    # Logic for Regular Users (and Staff acting as users)
    # Check for active session
    active_session = Conversation.objects.filter(
        user=user,
        is_active=True,
        user_deleted=False
    ).first()

    if active_session:
        counts['has_active_session'] = True
        # Count unread messages from counsellor (sender != user)
        counts['user_unread_count'] = active_session.messages.filter(
            is_read=False,
            is_deleted=False
        ).exclude(sender=user).count()

    return counts
