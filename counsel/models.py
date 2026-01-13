from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    """A counselling conversation between a user and a counsellor (staff)."""
    
    RETENTION_CHOICES = [
        ('24h', 'Delete after 24 hours'),
        ('permanent', 'Keep indefinitely'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='conversations'
    )
    counsellor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='counsellor_conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    retention_mode = models.CharField(
        max_length=20, 
        choices=RETENTION_CHOICES, 
        default='permanent'
    )
    user_deleted = models.BooleanField(default=False)  # User-side soft delete
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation {self.id}: {self.user.username}"


class Message(models.Model):
    """A single message in a counselling conversation."""
    
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete
    edited_at = models.DateTimeField(null=True, blank=True)  # Track edits
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message {self.id} from {self.sender.username}"
