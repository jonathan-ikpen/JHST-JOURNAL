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
        is_invite = instance.invitation_status == 'invited'
        action_word = "invited to" if is_invite else "assigned to"
        action_verb = "accept and" if is_invite else ""
        round_text = f" (Round {instance.round})" if instance.round > 1 else ""
        
        subject = f"Review Invitation{round_text}: {manuscript.title}" if is_invite else f"Review Assignment{round_text}: {manuscript.title}"
        message = (
            f"Dear {reviewer.get_full_name() or reviewer.username},\n\n"
            f"You have been {action_word} review the manuscript: '{manuscript.title}'{round_text}.\n"
            f"Please log in to the JHST dashboard to {action_verb} complete this review by {due_date}.\n\n"
            f"Best regards,\nJHST Editorial Team"
        )
        _send_notification_email(subject, message, [reviewer.email])

        # 3. Create In-app notification for Reviewer
        intro = "New Review Invitation" if is_invite else "New Review Assignment"
        msg = f"{intro}{round_text}: You have been {action_word} review '{manuscript.title}'."
        Notification.objects.create(
            recipient=reviewer,
            message=f"{msg} Due by {due_date}.",
            link='/dashboard/assigned-reviews/'
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
        
        # Check if all reviews for THIS round are completed
        current_round = instance.round
        pending_reviews = manuscript.reviews.filter(
            round=current_round, 
            date_completed__isnull=True,
            invitation_status__in=['assigned', 'invited', 'accepted']
        ).exclude(invitation_status='declined')
        
        if not pending_reviews.exists():
            for editor in editors:
                Notification.objects.create(
                    recipient=editor,
                    message=f"All Reviews In: All reviews for Round {current_round} of '{manuscript.title}' have been submitted. Decision ready.",
                    link=f'/dashboard/make_decision/{manuscript.id}/'
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
    author = instance.author
    
    if created:
        # Notify Author
        subject = f"Submission Received: {instance.title}"
        message = (
            f"Dear {author.get_full_name() or author.username},\n\n"
            f"Your manuscript '{instance.title}' has been successfully submitted to JHST. "
            f"You can track its status in your dashboard.\n\n"
            f"Best regards,\nJHST Editorial Team"
        )
        _send_notification_email(subject, message, [author.email])
        
        # In-app notification for Author
        Notification.objects.create(
            recipient=author,
            message=f"Submission Received: Your manuscript '{instance.title}' has been successfully submitted.",
            link='/dashboard/my-submissions/'
        )
        
        # Notify Editors
        editors = User.objects.filter(is_editor=True)
        for editor in editors:
            Notification.objects.create(
                recipient=editor,
                message=f"New Submission: '{instance.title}' by {author.get_full_name() or author.username}.",
                link='/dashboard/'
            )

    elif getattr(instance, 'status_changed', False):
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
            
            # Notify Reviewers who have provided feedback
            # They should now have a NEW review record for the current round
            previous_reviewers = instance.reviews.filter(date_completed__isnull=False).values_list('reviewer_id', flat=True).distinct()
            for rev_id in previous_reviewers:
                # Find the LATEST review for this reviewer (likely the one just created in submit_revision)
                latest_rev = instance.reviews.filter(reviewer_id=rev_id).order_by('-round', '-id').first()
                if latest_rev:
                    Notification.objects.create(
                        recipient=latest_rev.reviewer,
                        message=f"Author Correction: Revisions for '{instance.title}' (Round {instance.current_round}) have been uploaded.",
                        link=f'/dashboard/review-assignment/{latest_rev.id}/'
                    )
        
        elif status == 'accepted':
            # Notify Author via Email
            subject = f"Manuscript Accepted: {instance.title}"
            message = (
                f"Dear {author.get_full_name() or author.username},\n\n"
                f"Congratulations! We are pleased to inform you that your manuscript '{instance.title}' has been accepted for publication in the JHST Journal.\n\n"
                f"Your manuscript is now awaiting payment for it to be published. Please log in to your dashboard for payment instructions.\n\n"
                f"Best regards,\nJHST Editorial Team"
            )
            _send_notification_email(subject, message, [author.email])
            
            Notification.objects.create(
                recipient=author,
                message=f"Congratulations! Your manuscript '{instance.title}' has been accepted and is now awaiting payment for publication.",
                link=f'/dashboard/my-submission/{instance.id}/'
            )

        elif status == 'rejected':
            # Notify Author via Email
            subject = f"Decision Regarding Your Manuscript: {instance.title}"
            message = (
                f"Dear {author.get_full_name() or author.username},\n\n"
                f"Thank you for submitting your work to the JHST Journal. After a thorough review process, we regret to inform you that we are unable to accept your manuscript '{instance.title}' for publication at this time.\n\n"
                f"We appreciate the opportunity to consider your work and wish you success with your future submissions.\n\n"
                f"Best regards,\nJHST Editorial Team"
            )
            _send_notification_email(subject, message, [author.email])
            
            Notification.objects.create(
                recipient=author,
                message=f"Editorial Decision: Your manuscript '{instance.title}' has been rejected. View details for more information.",
                link=f'/dashboard/my-submission/{instance.id}/'
            )

        elif status == 'published':
            # Notify Author via Email
            subject = f"Manuscript Published: {instance.title}"
            # Try to get the issue if available via Article
            from .models import Article
            try:
                article = Article.objects.get(manuscript=instance)
                issue_text = f" in {article.issue}"
                link = f"/article/{article.id}/"
            except Article.DoesNotExist:
                issue_text = ""
                link = f'/dashboard/my-submission/{instance.id}/'
                
            message = (
                f"Dear {author.get_full_name() or author.username},\n\n"
                f"Congratulations! Your manuscript '{instance.title}' has been published{issue_text} in the JHST Journal.\n\n"
                f"You can view it here: {link}\n\n"
                f"Best regards,\nJHST Editorial Team"
            )
            _send_notification_email(subject, message, [author.email])
            
            Notification.objects.create(
                recipient=author,
                message=f"Published: Your manuscript '{instance.title}' is now live{issue_text}.",
                link=link
            )
