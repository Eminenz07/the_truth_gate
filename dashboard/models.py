from django.db import models

class SiteSettings(models.Model):
    # Singleton pattern enforcement
    live_stream_url = models.URLField(blank=True, help_text="Embed URL for live stream")
    is_live_now = models.BooleanField(default=False)
    
    giving_enabled = models.BooleanField(default=True)
    flutterwave_public_key = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name_plural = "Site Settings"

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            # If you try to save a new instance, replace the old one
            return 
        return super(SiteSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site Configuration"
