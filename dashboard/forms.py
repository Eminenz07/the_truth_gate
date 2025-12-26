from django import forms
from ckeditor.widgets import CKEditorWidget
from sermons.models import Sermon
from events.models import Event
from .models import SiteSettings

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['live_stream_url', 'is_live_now', 'giving_enabled', 'flutterwave_public_key']
        widgets = {
            'live_stream_url': forms.URLInput(attrs={'class': 'form-input'}),
            'flutterwave_public_key': forms.TextInput(attrs={'class': 'form-input'}),
        }

class SermonForm(forms.ModelForm):
    notes = forms.CharField(widget=CKEditorWidget())
    date_preached = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Sermon
        fields = [
            'title', 'series', 'speaker', 'date_preached', 
            'sermon_type', 'topics', 'video_url', 'audio_file',
            'scripture_reference', 'description', 'notes', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Sermon Title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'scripture_reference': forms.TextInput(attrs={'class': 'form-input'}),
            'video_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://youtube.com/...'}),
            'topics': forms.CheckboxSelectMultiple(),
        }

class EventForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = ['title', 'start_time', 'end_time', 'location', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
        }
