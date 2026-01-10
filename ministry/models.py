from django.db import models
from django.conf import settings

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

class Testimony(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the person sharing (or Anonymous)", blank=True)
    location = models.CharField(max_length=100, blank=True, help_text="e.g. London, UK")
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimony by {self.name or 'Anonymous'} ({'Approved' if self.is_approved else 'Pending'})"

class Donation(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    email = models.EmailField()
    reference = models.CharField(max_length=50, unique=True, help_text="Internal transaction reference")
    paystack_ref = models.CharField(max_length=100, blank=True, null=True, help_text="Reference from Paystack")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    verified = models.BooleanField(default=False, help_text="True if confirmed via Paystack API/Webhook")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.email} - {self.amount}"

from auditlog.registry import auditlog
auditlog.register(PrayerRequest)
auditlog.register(ContactSubmission)
auditlog.register(Testimony)
auditlog.register(Donation)
