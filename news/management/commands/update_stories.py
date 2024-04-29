from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
import feedparser
from datetime import datetime
from news.models import Source, Story

class Command(BaseCommand):
    help = 'Fetch stories from RSS feeds'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):
        user_id = options['user_id']
        # Filter sources based on the provided user ID
        sources = Source.objects.filter(user_id=user_id)
        for source in sources:
            feed = feedparser.parse(source.source_url)
            for entry in feed.entries:
                try:
                    # Ensure that the story doesn't already exist
                    if not Story.objects.filter(url=entry.link).exists():
                        # Ensure that all required fields are present and not empty
                        if all(field in entry and entry[field] for field in ['title', 'published', 'summary', 'link']):
                            # Try different datetime formats until one of them matches successfully
                            datetime_formats = [
                                '%a, %d %b %Y %H:%M:%S %z',  # Format 1
                                '%Y-%m-%dT%H:%M:%S%z',       # Format 2
                                # Add more datetime formats if needed
                            ]
                            published_date = None
                            for fmt in datetime_formats:
                                try:
                                    published_date = datetime.strptime(entry.published, fmt)
                                    break  # Break the loop if parsing successful
                                except ValueError:
                                    pass  # Continue to the next format if parsing failed
                            
                            if published_date is None:
                                raise ValueError('Failed to parse datetime')

                            story = Story(
                                title=entry.title[:500],  # Truncate to fit into max_length
                                published_date=published_date,
                                body_text=entry.summary[:2000],  # Truncate to fit into max_length
                                url=entry.link[:200],  # Truncate to fit into max_length
                                source=source,
                                created_by=source.user
                            )
                            story.full_clean()  # Validate model fields
                            story.save()
                            self.stdout.write(self.style.SUCCESS(f'Successfully created story: {story}'))
                        else:
                            self.stdout.write(self.style.WARNING('Missing or empty fields in RSS entry, skipping story creation'))
                    else:
                        self.stdout.write(self.style.WARNING('Story with this URL already exists, skipping story creation'))
                except ValidationError as e:
                    self.stdout.write(self.style.WARNING(f'Validation error: {e}'))
                except ValueError as e:
                    self.stdout.write(self.style.WARNING(f'Failed to parse datetime: {e}'))
