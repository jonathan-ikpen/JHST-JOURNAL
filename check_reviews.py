import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()

from journal.models import Review, Manuscript, User

# We know the manuscript ID is 9 from the screenshot
ms_id = 9
# Reviewer is 'timothy'
try:
    reviewer = User.objects.get(username='timothy')
except User.DoesNotExist:
    # If not timothy, find any reviewer with assignments for this ms
    reviewer_ids = Review.objects.filter(manuscript_id=ms_id).values_list('reviewer_id', flat=True).distinct()
    reviewer = User.objects.get(id=reviewer_ids[0])

reviews = Review.objects.filter(manuscript_id=ms_id, reviewer=reviewer).order_by('id')

print(f"--- Reviews for Manuscript #{ms_id} by {reviewer.username} ---")
for r in reviews:
    print(f"ID: {r.id} | Round: {r.round} | Status: {r.invitation_status} | Completed: {r.date_completed} | Latest Property: {r.is_latest_round}")

print("\n--- Manuscript State ---")
ms = Manuscript.objects.get(id=ms_id)
print(f"Status: {ms.status} | Current Round: {ms.current_round}")
