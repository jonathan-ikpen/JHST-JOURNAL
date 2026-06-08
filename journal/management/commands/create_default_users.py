import os
import re
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates default user accounts for reviewers and editorial board members from markdown file.'

    def handle(self, *args, **options):
        md_file_path = os.path.join(settings.BASE_DIR, 'users', 'Reviewers_Editorial_Board_Members-v2.md')
        
        if not os.path.exists(md_file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {md_file_path}"))
            return

        with open(md_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        users_created = 0
        users_skipped = 0

        for line in lines:
            line = line.strip()
            # Match table rows: | 1. | Name | Affiliation | Area | Email |
            if line.startswith('|') and len(line.split('|')) >= 6:
                parts = [p.strip() for p in line.split('|')]
                
                # Check if the first column is a number (e.g., "1.")
                s_no = parts[1]
                if re.match(r'^\d+\.?$', s_no):
                    name = parts[2]
                    affiliation = parts[3]
                    area = parts[4]
                    email = parts[5].strip()

                    # Clean up email (some might have weird characters or be empty)
                    if not email or '@' not in email:
                        continue

                    # Remove prefixes like "Prof.", "Dr.", "Engr." to get clean name
                    clean_name = re.sub(r'^(Prof\.|Dr\.|Engr\.|Professor)\s+', '', name, flags=re.IGNORECASE).strip()
                    name_parts = clean_name.split(' ')
                    first_name = name_parts[0]
                    last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                    
                    # Generate a username from email
                    username = email.split('@')[0].lower()
                    username = re.sub(r'[^a-zA-Z0-9\.\_]', '', username)

                    if not User.objects.filter(email=email).exists():
                        # We append digits to username if username already exists
                        base_username = username
                        counter = 1
                        while User.objects.filter(username=username).exists():
                            username = f"{base_username}{counter}"
                            counter += 1

                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password='password123',
                            first_name=first_name,
                            last_name=last_name,
                            is_reviewer=True,  # Give them reviewer status
                            is_email_verified=False  # They will need to verify later
                        )
                        self.stdout.write(self.style.SUCCESS(f"Created account for {name} ({email})"))
                        users_created += 1
                    else:
                        self.stdout.write(self.style.WARNING(f"Account for {email} already exists. Skipping."))
                        users_skipped += 1

        self.stdout.write(self.style.SUCCESS(f"\nFinished: {users_created} created, {users_skipped} skipped."))
