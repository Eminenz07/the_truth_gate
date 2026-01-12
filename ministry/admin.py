from django.contrib import admin
from .models import PrayerRequest, ContactSubmission

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'request_followup', 'is_prayed_for', 'created_at')
    list_filter = ('request_followup', 'is_prayed_for')
    search_fields = ('request_text', 'name')
    readonly_fields = ('created_at',)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at', 'is_responded')
    list_filter = ('is_responded',)
    search_fields = ('subject', 'message', 'name')
    readonly_fields = ('created_at',)
