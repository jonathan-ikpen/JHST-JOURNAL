import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()

from journal.models import Review, Manuscript

def check_rounds():
    print("Checking Review Round consistency...")
    for manuscript in Manuscript.objects.all():
        print(f"\nManuscript: {manuscript.title} (ID: {manuscript.id})")
        reviews = Review.objects.filter(manuscript=manuscript).order_by('reviewer_id', 'round')
        for review in reviews:
            latest = review.is_latest_round
            print(f"  Review ID: {review.id}, Reviewer: {review.reviewer.username}, Round: {review.round}, Is Latest: {latest}")

if __name__ == "__main__":
    check_rounds()
