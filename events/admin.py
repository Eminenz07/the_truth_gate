from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'location', 'is_recurring')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
