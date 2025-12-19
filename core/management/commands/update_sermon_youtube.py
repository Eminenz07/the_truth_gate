from django.core.management.base import BaseCommand
from core.models import Sermon

class Command(BaseCommand):
    help = 'Updates the sample sermon with a YouTube URL'

    def handle(self, *args, **kwargs):
        title = "Why God Feels Silent When You Need Him Most"
        try:
            sermon = Sermon.objects.get(title=title)
            sermon.youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            sermon.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated youtube_url for "{title}"'))
        except Sermon.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Sermon "{title}" not found'))
