import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()

from journal.models import Page, PageSection

def move_sidebar():
    try:
        index_page, _ = Page.objects.get_or_create(slug='index', defaults={'name': 'Home'})
        sidebar_page = Page.objects.get(slug='sidebar')
        
        # Clear out old sidebar sections from index page just in case this runs multiple times
        PageSection.objects.filter(page=index_page, section_key__startswith='sidebar_').delete()
        
        # Move sections and rename
        for section in PageSection.objects.filter(page=sidebar_page):
            section.page = index_page
            section.section_key = f"sidebar_{section.section_key}"
            # Adjust order if desired, e.g. starting at 10 so it's below the main Home page stuff
            section.order += 10
            section.save()
            
        # Delete old sidebar page
        sidebar_page.delete()
        print("Successfully moved sidebar sections to Home page!")
    except Page.DoesNotExist:
        print("Sidebar page does not exist or has already been moved.")

if __name__ == "__main__":
    move_sidebar()
