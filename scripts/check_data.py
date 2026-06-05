import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()

from journal.models import Manuscript

with open('data_results.txt', 'w') as f:
    f.write("Checking Manuscripts for Response to Reviewers:\n")
    f.write("-" * 50 + "\n")
    for m in Manuscript.objects.all().order_by('-id')[:15]:
        resp = m.response_to_reviewers.strip()
        f.write(f"ID: {m.id} | Status: {m.status}\n")
        f.write(f"Response (len={len(resp)}): {resp}\n")
        f.write("-" * 50 + "\n")
