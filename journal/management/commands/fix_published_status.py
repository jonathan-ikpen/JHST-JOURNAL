from django.core.management.base import BaseCommand
from journal.models import Manuscript

class Command(BaseCommand):
    help = 'Fixes manuscript statuses for published articles'

    def handle(self, *args, **options):
        # Find all manuscripts that have an associated article but are not marked as published
        manuscripts = Manuscript.objects.filter(article__isnull=False).exclude(status='published')
        
        updated_count = 0
        for manuscript in manuscripts:
            manuscript.status = 'published'
            manuscript.save()
            updated_count += 1
            self.stdout.write(f'Updated {manuscript.title}')
            
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} manuscripts to published status'))
