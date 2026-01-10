from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Order for manual sorting on homepage")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Sermon(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sermons')
    title = models.CharField(max_length=200, help_text="Problem-based title, e.g. 'Why God Feels Silent'")
    slug = models.SlugField(unique=True, blank=True)
    
    # The Problem
    problem_text = models.TextField(help_text="Short, relatable paragraphs. Reader must feel understood.")
    
    # Scripture Focus
    scripture_citation = models.CharField(max_length=100, help_text="e.g. 'Psalm 23:1-4'")
    scripture_text = models.TextField(help_text="The actual Bible text")
    
    # Explanation
    explanation_text = models.TextField(help_text="Plain English. No church jargon. Context + meaning.")
    
    # The Truth
    truth_text = models.TextField(help_text="Clear, sometimes uncomfortable. Scripture-aligned. Hopeful but honest.")
    
    # Apply This Today
    action_text = models.TextField(help_text="One practical action.")
    reflection_question = models.TextField(help_text="One reflection question.")
    
    # Optional
    audio_url = models.URLField(blank=True, help_text="Optional link to audio version")
    youtube_url = models.URLField(blank=True, help_text="Optional link to YouTube video")
    
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

from auditlog.registry import auditlog
auditlog.register(Category)
auditlog.register(Sermon)
auditlog.register(NewsletterSubscriber)
