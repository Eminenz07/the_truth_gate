from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = RichTextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, default="Main Sanctuary")
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    
    is_recurring = models.BooleanField(default=False)
    recurrence_rule = models.CharField(max_length=100, blank=True, help_text="e.g. 'Weekly on Sundays'")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    @property
    def google_calendar_url(self):
        """Generates a Google Calendar add event link."""
        title = self.title.replace(' ', '+')
        start = self.start_time.strftime('%Y%m%dT%H%M%SZ')
        end = self.end_time.strftime('%Y%m%dT%H%M%SZ')
        details = (self.description or "").replace(' ', '+')
        location = self.location.replace(' ', '+')
        return f"https://www.google.com/calendar/render?action=TEMPLATE&text={title}&dates={start}/{end}&details={details}&location={location}&sf=true&output=xml"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
