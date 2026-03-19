from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Review, Manuscript, Notification, User
from .views import _send_notification_email

@receiver(post_save, sender=Review)
def handle_review_updates(sender, instance, created, **kwargs):
    manuscript = instance.manuscript
    reviewer = instance.reviewer
    
    if created:
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
    
    # Notify Editor when a review is completed
    elif instance.date_completed and getattr(instance, 'date_completed_changed', False):
        editors = User.objects.filter(is_editor=True)
        for editor in editors:
            Notification.objects.create(
                recipient=editor,
                message=f"Review Completed: {reviewer.username} has submitted a review for '{manuscript.title}'.",
                link=f'/dashboard/manuscript/{manuscript.id}/'
            )
            
    # Notify Reviewer when a re-review is requested (reset of date_completed)
    elif not instance.date_completed and getattr(instance, 'date_completed_changed', False):
        subject = f"Re-review Requested: {manuscript.title}"
        message = (
            f"Dear {reviewer.get_full_name() or reviewer.username},\n\n"
            f"The author has submitted a corrected version of the manuscript: '{manuscript.title}'.\n"
            f"The editor has requested that you re-review the revised version.\n\n"
            f"Please log in to the JHST dashboard to view the changes and update your review.\n\n"
            f"Best regards,\nJHST Editorial Team"
        )
        _send_notification_email(subject, message, [reviewer.email])

        Notification.objects.create(
            recipient=reviewer,
            message=f"Re-review Requested: Please evaluate the revised version of '{manuscript.title}'.",
            link=f'/dashboard/reviewer-manuscript/{manuscript.id}/'
        )

@receiver(post_save, sender=Manuscript)
def handle_manuscript_status_change(sender, instance, created, **kwargs):
    if not created and getattr(instance, 'status_changed', False):
        status = instance.status
        author = instance.author
        
        if status == 'needs_revision':
            # Notify Author
            subject = f"Revisions Required: {instance.title}"
            message = (
                f"Dear {author.get_full_name() or author.username},\n\n"
                f"The editorial team has reached a decision regarding your manuscript '{instance.title}'. "
                f"Revisions are required before it can be accepted for publication.\n\n"
                f"Please log in to your dashboard to view the reviewer feedback and submit your corrected manuscript.\n\n"
                f"Best regards,\nJHST Editorial Team"
            )
            _send_notification_email(subject, message, [author.email])
            
            Notification.objects.create(
                recipient=author,
                message=f"Revisions Required: Your manuscript '{instance.title}' needs corrections. See reviewer feedback.",
                link=f'/dashboard/my-submission/{instance.id}/'
            )
            
        elif status == 'revision_submitted':
            # Notify Editors
            editors = User.objects.filter(is_editor=True)
            for editor in editors:
                Notification.objects.create(
                    recipient=editor,
                    message=f"Revision Submitted: Author has uploaded a corrected version of '{instance.title}'.",
                    link=f'/dashboard/manuscript/{instance.id}/'
                )
