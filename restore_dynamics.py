import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()

from journal.models import Page, PageSection

def populate_organogram():
    page = Page.objects.get(slug='index')
    organogram_html = """
<div class="space-y-3">
  <div class="organogram-item flex items-start gap-3">
    <div class="organogram-number bg-[#054D08] text-white font-bold px-3 py-2 rounded text-sm min-w-[40px] text-center">01</div>
    <div class="flex-1">
      <div class="organogram-title bg-gray-100 dark:bg-gray-700 font-bold px-4 py-2 rounded-t text-sm">Editor-in-Chief</div>
      <div class="organogram-description border border-gray-200 dark:border-gray-600 px-4 py-2 rounded-b text-sm text-gray-700 dark:text-gray-300">Provides overall direction and final authority on all publications</div>
    </div>
  </div>
  <div class="organogram-item flex items-start gap-3">
    <div class="organogram-number bg-[#1565C0] text-white font-bold px-3 py-2 rounded text-sm min-w-[40px] text-center">02</div>
    <div class="flex-1">
      <div class="organogram-title bg-gray-100 dark:bg-gray-700 font-bold px-4 py-2 rounded-t text-sm">Managing Editor</div>
      <div class="organogram-description border border-gray-200 dark:border-gray-600 px-4 py-2 rounded-b text-sm text-gray-700 dark:text-gray-300">Oversees day-to-day journal operations and coordinates editorial workflow</div>
    </div>
  </div>
  <div class="organogram-item flex items-start gap-3">
    <div class="organogram-number bg-[#6A1B9A] text-white font-bold px-3 py-2 rounded text-sm min-w-[40px] text-center">03</div>
    <div class="flex-1">
      <div class="organogram-title bg-gray-100 dark:bg-gray-700 font-bold px-4 py-2 rounded-t text-sm">Associate Editor</div>
      <div class="organogram-description border border-gray-200 dark:border-gray-600 px-4 py-2 rounded-b text-sm text-gray-700 dark:text-gray-300">Supports the Managing Editor</div>
    </div>
  </div>
  <div class="organogram-item flex items-start gap-3">
    <div class="organogram-number bg-[#4A90E2] text-white font-bold px-3 py-2 rounded text-sm min-w-[40px] text-center">04</div>
    <div class="flex-1">
      <div class="organogram-title bg-gray-100 dark:bg-gray-700 font-bold px-4 py-2 rounded-t text-sm">Section Editor</div>
      <div class="organogram-description border border-gray-200 dark:border-gray-600 px-4 py-2 rounded-b text-sm text-gray-700 dark:text-gray-300">Checks the appropriateness of a manuscript, handles peer-review and makes suggestions to the Managing Editor</div>
    </div>
  </div>
  <div class="organogram-item flex items-start gap-3">
    <div class="organogram-number bg-[#795548] text-white font-bold px-3 py-2 rounded text-sm min-w-[40px] text-center">05</div>
    <div class="flex-1">
      <div class="organogram-title bg-gray-100 dark:bg-gray-700 font-bold px-4 py-2 rounded-t text-sm">Editorial Board</div>
      <div class="organogram-description border border-gray-200 dark:border-gray-600 px-4 py-2 rounded-b text-sm text-gray-700 dark:text-gray-300">Make all-inclusive advice to Editor-in-Chief and Managing Editor for better journal indices</div>
    </div>
  </div>
</div>
""".strip()

    PageSection.objects.update_or_create(
        page=page, section_key='organogram',
        defaults={'content_type': 'html', 'text_content': organogram_html, 'order': 1}
    )
    print("Organogram populated.")

    # Also set video_url for introduction section
    try:
        intro = PageSection.objects.get(page=page, section_key='introduction')
        intro.video_url = 'https://player.vimeo.com/video/1129153382'
        intro.save()
        print("Introduction video_url set.")
    except PageSection.DoesNotExist:
        print("Introduction section not found, please run populate_index.py first.")


def populate_sidebar():
    sidebar_page, _ = Page.objects.get_or_create(slug='sidebar', defaults={'name': 'Sidebar'})
    PageSection.objects.filter(page=sidebar_page).delete()

    # Announcement block
    PageSection.objects.create(
        page=sidebar_page, section_key='announcement', content_type='html', order=0,
        text_content='<h3 class="text-xl font-bold">CHANGES TO AUTHOR GUIDELINES AND POLICIES</h3>'
    )

    # New Release (image placeholder — user to upload from admin)
    PageSection.objects.create(
        page=sidebar_page, section_key='new_release', content_type='image', order=1,
        text_content='New Release',
    )

    # Make a Submission button
    PageSection.objects.create(
        page=sidebar_page, section_key='submission_btn', content_type='html', order=2,
        text_content='<a href="/submit/" class="block w-full bg-gray-200 dark:bg-gray-700 text-text-light dark:text-text-dark font-bold py-2 px-4 rounded border-b-4 border-gray-400 hover:bg-gray-300 text-center">MAKE A SUBMISSION</a>'
    )

    # Information links
    PageSection.objects.create(
        page=sidebar_page, section_key='information', content_type='html', order=3,
        text_content="""
<h3 class="text-lg font-display font-bold border-b border-gray-200 dark:border-gray-700 pb-2 mb-4">Information</h3>
<ul class="space-y-2">
  <li><a class="text-primary hover:underline" href="/subscription-advertising/">For Readers</a></li>
  <li><a class="text-primary hover:underline" href="/author-guidelines/">For Authors</a></li>
  <li><a class="text-primary hover:underline" href="/subscription-advertising/">For Librarians</a></li>
</ul>""".strip()
    )

    # Keywords block (image — user to upload keyword cloud from admin)
    PageSection.objects.create(
        page=sidebar_page, section_key='keywords', content_type='image', order=4,
        text_content='Keywords',
    )

    # Browse links
    PageSection.objects.create(
        page=sidebar_page, section_key='browse', content_type='html', order=5,
        text_content="""
<h3 class="text-lg font-display font-bold border-b border-gray-200 dark:border-gray-700 pb-2 mb-4">Browse</h3>
<ul class="space-y-2">
  <li><a class="text-primary hover:underline" href="/aim-scope/">Categories</a></li>
</ul>""".strip()
    )

    print(f"Sidebar populated with {PageSection.objects.filter(page=sidebar_page).count()} blocks.")


if __name__ == '__main__':
    populate_organogram()
    populate_sidebar()
    print("\nDone! Please go to Admin > Pages to upload your sidebar images.")
