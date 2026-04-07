import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from journal.models import Page, PageSection
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Migrates hardcoded content from HTML templates to the CMS'

    def handle(self, *args, **options):
        template_dir = os.path.join(settings.BASE_DIR, 'templates', 'journal')
        
        # MAPPING: slug -> file_name
        # This should match urls.py
        slugs = {
            'index': 'index.html',
            'about': 'about.html',
            'aim-scope': 'aim_scope.html',
            'editorial-team': 'editorial_team.html',
            'publication-schedule': 'publication_schedule.html',
            'publication-fees': 'publication_fees.html',
            'contact': 'contact.html',
            'publications': 'publications.html',
            'indexing': 'indexing.html',
            'metrics': 'metrics.html',
            'guidelines': 'guidelines.html',
            'author-guidelines': 'author_guidelines.html',
            'reviewer-guidelines': 'reviewer_guidelines.html',
            'ethics-malpractice': 'ethics_malpractice.html',
            'open-access-policy': 'open_access_policy.html',
            'editorial-policy': 'editorial_policy.html',
            'peer-review-policy': 'peer_review_policy.html',
            'archiving-policy': 'archiving_policy.html',
            'subscription-advertising': 'subscription_advertising.html',
            'plagiarism-policy': 'plagiarism_policy.html',
            'policies': 'policies.html',
            'jhst-journals': 'jhst_journals.html',
        }

        for slug, filename in slugs.items():
            filepath = os.path.join(template_dir, filename)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f"File {filename} not found, skipping."))
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract H1 as the page name if it exists
            h1_tag = soup.find('h1')
            page_name = h1_tag.get_text(strip=True) if h1_tag else slug.capitalize()
            
            # Identify the main content area
            # Priority 1: .prose div (Standard for most pages)
            # Priority 2: .bg-card-light or .bg-card-dark (Used for more complex layouts)
            content_div = soup.find('div', class_='prose')
            if not content_div:
                # Fallback to the main card container
                content_div = soup.find('div', class_='bg-card-light') or soup.find('div', class_='bg-card-dark')
            
            if not content_div:
                self.stdout.write(self.style.WARNING(f"No suitable content div found in {filename}, skipping content extraction."))
                Page.objects.get_or_create(slug=slug, defaults={'name': page_name})
                continue

            # If we used the card fallback, we MUST exclude the H1 which was already extracted
            if content_div.find('h1'):
                 content_div.find('h1').decompose()

            # Extract the inner HTML
            inner_html = "".join([str(x) for x in content_div.contents]).strip()
            
            # Create or update Page
            page, created = Page.objects.get_or_create(slug=slug, defaults={'name': page_name})
            
            # SPECIAL CASE: HOME PAGE (index)
            # Home page has very specific sections that should be editable individually
            if slug == 'index':
                sections_map = {
                    'introduction': 'An Introduction to the Journal',
                    'about_mission': 'About the Journal',
                    'editors_desk': 'From the Chief Editor',
                }
                
                h2s = soup.find_all('h2')
                count = 0
                for h2 in h2s:
                    h2_text = h2.get_text(strip=True).lower()
                    for key, marker in sections_map.items():
                        if marker.lower() in h2_text:
                            section_soup = h2.find_parent('section')
                            if section_soup:
                                # Decompose title
                                h2.decompose()
                                
                                inner_content = "".join([str(x) for x in section_soup.contents]).strip()
                                PageSection.objects.update_or_create(
                                    page=page,
                                    section_key=key,
                                    defaults={
                                        'content_type': 'html',
                                        'text_content': inner_content,
                                        'order': count
                                    }
                                )
                                count += 1
                                break
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated Home Page with {count} sections."))
                continue

            # FINAL FALLBACK (Standard CMS pages)
            PageSection.objects.update_or_create(
                page=page,
                section_key='main_content',
                defaults={
                    'content_type': 'html',
                    'text_content': inner_html,
                    'order': 0
                }
            )

            self.stdout.write(self.style.SUCCESS(f"Successfully migrated {filename} to slug '{slug}'"))
