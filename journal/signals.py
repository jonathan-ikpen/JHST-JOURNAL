from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Review, Manuscript, Notification
from .views import _send_notification_email

@receiver(post_save, sender=Review)
def handle_reviewer_assignment(sender, instance, created, **kwargs):
    if created:
        manuscript = instance.manuscript
        reviewer = instance.reviewer
        due_date = instance.due_date or (timezone.now().date() + timezone.timedelta(days=14))
        
        # 1. Update manuscript status if it was just submitted
        if manuscript.status == 'submitted':
            manuscript.status = 'under_review'
            manuscript.save()
            
        # 2. Notify Reviewer via Email
        subject = f"Review Invitation: {manuscript.title}"
        message = (
            f"Dear {reviewer.get_full_name() or reviewer.username},\n\n"
            f"You have been assigned to review the manuscript: '{manuscript.title}'.\n"
            f"Please log in to the JHST dashboard to accept and complete this review by {due_date}.\n\n"
            f"Best regards,\nJHST Editorial Team"
        )
        _send_notification_email(subject, message, [reviewer.email])

        # 3. Create In-app notification for Reviewer
        Notification.objects.create(
            recipient=reviewer,
            message=f"New Review Assignment: You have been assigned to review '{manuscript.title}'. Due by {due_date}.",
            link='/dashboard/'
        )
