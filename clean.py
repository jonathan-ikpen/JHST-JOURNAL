import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()

from journal.models import PageSection

s = PageSection.objects.filter(page__slug='index', section_key='editors_desk').first()
if s and s.text_content:
    content = s.text_content
    # Remove the photo wrapper HTML
    content = re.sub(r'<div class="editor-photo[^>]+>[\s\S]*?</div>', '', content)
    # Remove the outer wrappers
    content = content.replace('<div class="editor-content flex flex-col md:flex-row gap-8 items-start">', '')
    content = content.replace('<div class="editor-message flex-grow">', '')
    # Remove closing divs at the end
    content = content.replace('</div>', '', 2)
    s.text_content = content.strip()
    s.save()
    print("Cleaned editors desk text")
