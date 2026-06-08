import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates default test accounts for author, reviewer, and editor.'

    def handle(self, *args, **options):
        # 1. Test Author
        if not User.objects.filter(username='author').exists():
            author = User.objects.create_user(
                username='author',
                email='author1@test.com',
                password='password123',
                first_name='Test',
                last_name='Author',
                is_author=True,
                is_email_verified=True
            )
            self.stdout.write(self.style.SUCCESS('Successfully created Test Author (author1@test.com)'))
        else:
            self.stdout.write(self.style.WARNING('Test Author already exists.'))

        # 2. Test Reviewer
        if not User.objects.filter(username='reviewer').exists():
            reviewer = User.objects.create_user(
                username='reviewer',
                email='reviewer1@test.com',
                password='password123',
                first_name='Test',
                last_name='Reviewer',
                is_reviewer=True,
                is_email_verified=True
            )
            self.stdout.write(self.style.SUCCESS('Successfully created Test Reviewer (reviewer1@test.com)'))
        else:
            self.stdout.write(self.style.WARNING('Test Reviewer already exists.'))

        # 3. Test Editor
        if not User.objects.filter(username='editor').exists():
            editor = User.objects.create_user(
                username='editor',
                email='editor1@test.com',
                password='password123',
                first_name='Test',
                last_name='Editor',
                is_editor=True,
                is_email_verified=True
            )
            self.stdout.write(self.style.SUCCESS('Successfully created Test Editor (editor1@test.com)'))
        else:
            self.stdout.write(self.style.WARNING('Test Editor already exists.'))
