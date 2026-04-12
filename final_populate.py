import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()

from journal.models import Page, PageSection

def populate_all():
    # 1. Update/Create Home Page Sections (without deleting existing ones like organogram)
    page, _ = Page.objects.get_or_create(slug='index', defaults={'name': 'Home'})
    
    # Organogram
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

    # Introduction
    intro_html = """
<div class="video-placeholder text-gray-500 italic">
  Your video will appear here. To change it, update the Video URL field below.
</div>
    """.strip()
    PageSection.objects.update_or_create(
        page=page, section_key='introduction',
        defaults={'content_type': 'video', 'video_url': 'https://player.vimeo.com/video/1129153382', 'text_content': intro_html, 'order': 0}
    )

    # Mission
    mission_html = """
<div class="mission-statement">
  <h3 class="text-xl font-bold mb-4 text-primary">MISSION STATEMENT</h3>
  <p class="mb-4 text-gray-700 leading-relaxed">Journal of Hydrocarbon Science and Technology (JHST) is the official publication of the Petroleum Training Institute, PTI, Effurun, Nigeria. The journal seeks to:</p>
  <ol class="list-decimal pl-6 space-y-3 text-gray-700">
    <li>Provide a global platform for original, peer-reviewed research that deepens understanding and drives innovation across the hydrocarbon value chain — from exploration and production to refining, environmental management, renewable integration, and digital transformation</li>
    <li>Provide the general public with dynamic and required information to the world for the purpose of innovation, knowledge/education, lifestyle, culture and career development.</li>
  </ol>
</div>
    """.strip()
    PageSection.objects.update_or_create(
        page=page, section_key='about_mission',
        defaults={'content_type': 'html', 'text_content': mission_html, 'order': 2}
    )

    # Editors Desk (without hardcoded image, to allow image_content uploading)
    editor_html = """
<div class="editor-message">
  <p class="mb-4 text-gray-700 leading-relaxed text-justify">In an era where the global energy landscape is undergoing unprecedented transformation, the Journal of Hydrocarbon Science and Technology (JHST) emerges as a timely response to a critical need — the need to rethink, redefine, and renew our approach to energy development, sustainability, and innovation.</p>
  <p class="mb-4 text-gray-700 leading-relaxed text-justify">The Petroleum Training Institute (PTI), for over five decades, has served as Nigeria’s premier institution for technical excellence in the petroleum and allied sectors. Through education, applied research, and industry collaboration, PTI has equipped generations of professionals with the competence and creativity to advance the oil and gas industry.</p>
  <p class="mb-6 text-gray-700 leading-relaxed text-justify">The JHST is a natural evolution of this legacy — a bridge between research and real-world application, between academia and industry, between innovation and impact.</p>
  <div class="mt-8 pt-6 border-t border-gray-100">
    <p class="font-bold text-xl text-primary mb-1">Engr. Henry I. Adimula</p>
    <p class="text-gray-600 font-medium italic">Principal/Chief Executive</p>
    <p class="text-gray-500 italic">Petroleum Training Institute</p>
  </div>
</div>
    """.strip()
    PageSection.objects.update_or_create(
        page=page, section_key='editors_desk',
        defaults={'content_type': 'html', 'text_content': editor_html, 'order': 3}
    )

    print("Index page successfully populated with correct video URL and clean HTML for Editor's desk!")

    # 2. Sidebar content
    sidebar_page, _ = Page.objects.get_or_create(slug='sidebar', defaults={'name': 'Sidebar'})
    PageSection.objects.filter(page=sidebar_page).delete()

    PageSection.objects.create(page=sidebar_page, section_key='announcement', content_type='html', order=0, text_content='<h3 class="text-xl font-bold">CHANGES TO AUTHOR GUIDELINES AND POLICIES</h3>')
    PageSection.objects.create(page=sidebar_page, section_key='new_release', content_type='image', order=1, text_content='New Release (Upload Image Below)')
    PageSection.objects.create(page=sidebar_page, section_key='submission_btn', content_type='html', order=2, text_content='<a href="/submit/" class="block w-full bg-gray-200 dark:bg-gray-700 text-text-light dark:text-text-dark font-bold py-2 px-4 rounded border-b-4 border-gray-400 hover:bg-gray-300 text-center">MAKE A SUBMISSION</a>')
    PageSection.objects.create(page=sidebar_page, section_key='information', content_type='html', order=3, text_content='<h3 class="text-lg font-display font-bold border-b border-gray-200 dark:border-gray-700 pb-2 mb-4">Information</h3><ul class="space-y-2"><li><a class="text-primary hover:underline" href="/subscription-advertising/">For Readers</a></li><li><a class="text-primary hover:underline" href="/author-guidelines/">For Authors</a></li><li><a class="text-primary hover:underline" href="/subscription-advertising/">For Librarians</a></li></ul>')
    PageSection.objects.create(page=sidebar_page, section_key='keywords', content_type='image', order=4, text_content='Keyword Cloud (Upload Image Below)')
    PageSection.objects.create(page=sidebar_page, section_key='browse', content_type='html', order=5, text_content='<h3 class="text-lg font-display font-bold border-b border-gray-200 dark:border-gray-700 pb-2 mb-4">Browse</h3><ul class="space-y-2"><li><a class="text-primary hover:underline" href="/aim-scope/">Categories</a></li></ul>')

    print("Sidebar sections created successfully!")


if __name__ == '__main__':
    populate_all()
