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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields optional by default (for drafts)
        self.fields['series'].required = False
        self.fields['video_url'].required = False
        self.fields['audio_file'].required = False
        self.fields['description'].required = False
        self.fields['scripture_reference'].required = False
        self.fields['date_preached'].required = False # Will handle in clean
        self.fields['speaker'].required = False

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        title = cleaned_data.get('title')
        
        # If no date provided for draft, default to today to satisfy Model
        if not cleaned_data.get('date_preached'):
            from django.utils import timezone
            cleaned_data['date_preached'] = timezone.now().date()
        
        # Validation for Published Sermons
        if status == 'published':
            errors = {}
            if not cleaned_data.get('description'):
                errors['description'] = "Description is required for published sermons."
            if not cleaned_data.get('scripture_reference'):
                errors['scripture_reference'] = "Scripture reference is required for published sermons."
            # Series and Media explicitly requested as OPTIONAL even for published.
            
            if errors:
                raise forms.ValidationError(errors)
        
        return cleaned_data

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
