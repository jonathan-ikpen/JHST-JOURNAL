import os
from django.core.management.base import BaseCommand
from django.core.files import File
from pages.models import ConferencesPage, ConferenceProceeding
from django.conf import settings

class Command(BaseCommand):
    help = 'Populates the Conferences page and loads the initial ICHST 2023 Proceedings.'

    def handle(self, *args, **kwargs):
        # 1. Create Conferences Page singleton if it doesn't exist
        page, created = ConferencesPage.objects.get_or_create(pk=1)
        if created or not page.intro_text:
            page.intro_text = "<p>Welcome to the JHST Conferences and Proceedings section. Here you can find the official books of proceedings from our affiliated international conferences and summits.</p>"
            page.save()
            self.stdout.write(self.style.SUCCESS("Successfully created ConferencesPage singleton."))
        else:
            self.stdout.write(self.style.WARNING("ConferencesPage singleton already exists."))
        
        # 2. Add the ICHST 2023 proceeding if it doesn't exist
        if not ConferenceProceeding.objects.filter(title="ICHST 2023").exists():
            # Source paths relative to BASE_DIR
            pdf_src = os.path.join(settings.BASE_DIR, 'static', 'documents', 'ICHST2023_BOOK OF PROCEEDINGS_v4.pdf')
            img_src = os.path.join(settings.BASE_DIR, 'static', 'assets', 'images', 'ICHST2023_BOOK OF PROCEEDINGS_v4_COVER.png')
            
            proc = ConferenceProceeding(
                title="ICHST 2023",
                theme="The Future of Oil and Gas Industry: Opportunities, Challenges and Development",
                date="23rd - 24th October 2023",
                order=1
            )
            
            if os.path.exists(pdf_src):
                with open(pdf_src, 'rb') as pdf_file:
                    proc.pdf_document.save('ICHST2023_BOOK_OF_PROCEEDINGS_v4.pdf', File(pdf_file), save=False)
                self.stdout.write(self.style.SUCCESS(f"Loaded PDF: {pdf_src}"))
            else:
                self.stdout.write(self.style.ERROR(f"Warning: PDF not found at {pdf_src}"))
                
            if os.path.exists(img_src):
                with open(img_src, 'rb') as img_file:
                    proc.cover_image.save('ICHST2023_BOOK_OF_PROCEEDINGS_v4_COVER.png', File(img_file), save=False)
                self.stdout.write(self.style.SUCCESS(f"Loaded Image: {img_src}"))
            else:
                self.stdout.write(self.style.ERROR(f"Warning: Image not found at {img_src}"))
                
            proc.save()
            self.stdout.write(self.style.SUCCESS("Successfully created ICHST 2023 Conference Proceeding entry."))
        else:
            self.stdout.write(self.style.WARNING("ICHST 2023 Proceeding already exists."))
