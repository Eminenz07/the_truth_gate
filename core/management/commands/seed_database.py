from django.core.management.base import BaseCommand
from core.models import Category, Sermon
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with initial categories and a sample sermon'

    def handle(self, *args, **kwargs):
        categories_data = [
            ("Faith & Doubt", "When you question if God is there or if He cares."),
            ("Fear, Anxiety & Peace", "Finding calm when your mind won't stop racing."),
            ("Financial Pressure", "Trusting God when the numbers don't add up."),
            ("Purpose & Direction", "Figuring out what you're supposed to do with your life."),
            ("Relationships & Forgiveness", "Navigating conflict, loneliness, and healing."),
            ("Sin, Guilt & Grace", "Dealing with failure and finding true freedom."),
        ]

        categories = {}
        for i, (name, desc) in enumerate(categories_data):
            cat, created = Category.objects.get_or_create(
                slug=slugify(name),
                defaults={
                    'name': name,
                    'description': desc,
                    'order': i
                }
            )
            categories[name] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))
            else:
                self.stdout.write(f'Category already exists: {name}')

        # Sample Sermon
        sermon_title = "Why God Feels Silent When You Need Him Most"
        if not Sermon.objects.filter(slug=slugify(sermon_title)).exists():
            Sermon.objects.create(
                category=categories["Faith & Doubt"],
                title=sermon_title,
                problem_text="You’ve been praying. You’ve been waiting. But the only response you get is deafening silence.\n\nIt feels like your prayers are hitting the ceiling. You start to wonder: Is God even listening? Is He angry with me? Or worse, is He not even there?\n\nIt’s a lonely, heavy feeling that makes you question everything you thought you knew about faith.",
                scripture_citation="Psalm 13:1-2",
                scripture_text="How long, O Lord? Will you forget me forever? How long will you hide your face from me? How long must I take counsel in my soul and have sorrow in my heart all the day?",
                explanation_text="This isn’t a quote from a skeptic; it’s a prayer from David, a man in the Bible described as being 'after God's own heart'.\n\nDavid wasn't afraid to be honest with God. He didn't sugarcoat his experience. He felt abandoned, and he told God exactly that.\n\nNotice that his honesty didn't disqualify him from God's presence. In fact, it was the bridge to it.",
                truth_text="God’s silence is not the same as His absence.\n\nJust because you can't feel Him doesn't mean He isn't working. In every story in Scripture, the periods of waiting and silence were where the deepest roots of trust were grown.\n\nYou are not a bad Christian for feeling this way. You are just in the middle of the story, not the end.",
                action_text="Set a timer for 5 minutes. Sit in silence. Don't try to pray or 'feel' spiritual. Just sit and acknowledge that God is God, and you are you. Tell Him, 'I feel like You are silent, but I am choosing to sit here with You anyway.'",
                reflection_question="If you knew for a fact that God was working behind the scenes right now, how would that change the way you feel about this silence?",
                audio_url="",
                youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Placeholder
            )
            self.stdout.write(self.style.SUCCESS(f'Created sermon: {sermon_title}'))
        else:
             self.stdout.write(f'Sermon already exists: {sermon_title}')
