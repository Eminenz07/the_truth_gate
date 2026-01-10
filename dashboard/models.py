from django.db import models

class SiteSettings(models.Model):
    # Singleton pattern
    # Hero Section
    hero_headline = models.CharField(max_length=200, default="Igniting a Burning Generation On Fire For Jesus")
    hero_subtext = models.TextField(default="We are a global movement raising a passionate generation empowered to influence nations with the fire and truth of Jesus.")
    
    # Vision Section
    vision_title = models.CharField(max_length=100, default="Our Vision")
    vision_text = models.TextField(default="Raising a Burning Generation. Empowering young believers to live passionately for Jesus.")
    
    # Mission Section
    mission_title = models.CharField(max_length=100, default="Our Mission")
    mission_text = models.TextField(default="Raising, Building and Equipping People as Kingdom Ambassadors in Every Sphere of Human Influence.")
    
    # Live Stream
    live_stream_url = models.URLField(blank=True, help_text="YouTube or generic stream link")
    live_stream_url = models.URLField(blank=True, help_text="YouTube or generic stream link")
    is_live_now = models.BooleanField(default=False)

    # Social Media
    facebook_url = models.URLField(blank=True, default="https://facebook.com")
    instagram_url = models.URLField(blank=True, default="https://instagram.com")
    youtube_url = models.URLField(blank=True, default="https://youtube.com")
    x_url = models.URLField(blank=True, default="https://x.com", help_text="X (formerly Twitter) URL")
    
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
