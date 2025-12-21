from django.contrib import admin
from .models import Speaker, Series, Topic, Sermon

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'series', 'date_preached', 'status', 'sermon_type')
    list_filter = ('status', 'sermon_type', 'series', 'speaker', 'topics')
    search_fields = ('title', 'scripture_reference', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_preached'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'date_preached')
        }),
        ('Classification', {
            'fields': ('series', 'speaker', 'topics', 'scripture_reference')
        }),
        ('Media', {
            'fields': ('sermon_type', 'video_url', 'audio_file')
        }),
        ('Content', {
            'fields': ('description', 'notes')
        }),
    )
