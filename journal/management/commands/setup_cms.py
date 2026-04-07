from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Set up the CMS by loading all initial page and section data from the fixture.'

    def handle(self, *args, **options):
        fixture_path = os.path.join('journal', 'fixtures', 'cms_initial_data.json')

        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(
                f'Fixture file not found at: {fixture_path}\n'
                'Please ensure cms_initial_data.json is present in journal/fixtures/'
            ))
            return

        self.stdout.write('Loading CMS initial data fixture...')
        try:
            call_command('loaddata', fixture_path, verbosity=1)
            self.stdout.write(self.style.SUCCESS(
                '\nCMS setup complete! All pages and sections have been populated.'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nError loading fixture: {e}'))
