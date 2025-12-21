from django.db import models

class PrayerRequest(models.Model):
    name = models.CharField(max_length=100, help_text="Leave blank for anonymous requests", blank=True)
    email = models.EmailField(blank=True)
    request_text = models.TextField()
    is_private = models.BooleanField(default=True, help_text="Keep this request private (Staff only)")
    is_prayed_for = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.name or 'Anonymous'} - {self.created_at.date()}"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.name}"
