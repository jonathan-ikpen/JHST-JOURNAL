from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import ResearcherRegistrationForm, ManuscriptForm, ReviewForm, VolumeForm, IssueForm, UserProfileForm, RevisionForm
from .models import Manuscript, Review, User, Issue, Article, Volume, Notification, Announcement
from .decorators import verified_email_required

def _send_notification_email(subject, message, recipient_list, html_message=None):
    """
    Helper function to send emails without blocking.
    Prints error to console if fails (development mode).
    """
    try:
        # If EMAIL_HOST_USER is not set, use a dummy sender
        sender = getattr(settings, 'EMAIL_HOST_USER', 'noreply@jhst.org')
        send_mail(subject, message, sender, recipient_list, fail_silently=False, html_message=html_message)
    except Exception as e:
        print(f"Error sending email: {e}")


def register(request):
    if request.method == 'POST':
        form = ResearcherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = request.build_absolute_uri(
                reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
            )
            
            html_message = render_to_string('emails/verify_email.html', {
                'user': user,
                'verification_url': verification_url
            })
            text_message = render_to_string('emails/verify_email.txt', {
                'user': user,
                'verification_url': verification_url
            })
            
            try:
                sender = getattr(settings, 'EMAIL_HOST_USER', 'noreply@jhst.org')
                send_mail(
                    subject="Verify your JHST account",
                    message=text_message,
                    from_email=sender,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                
            login(request, user)
            messages.success(request, f"Welcome to JHST, {user.username}! Your account has been created. Please check your email to verify your account.")
            return redirect('dashboard')
    else:
        form = ResearcherRegistrationForm()
    return render(request, 'journal/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'journal/profile.html', {
        'form': form,
        'user': request.user
    })

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def dashboard(request):
    # Always get personal submissions
    my_submissions = Manuscript.objects.filter(author=request.user).order_by('-submitted_date')

    if request.user.is_editor:
        submissions_list = Manuscript.objects.all()
        
        # Filtering
        status_filter = request.GET.get('status')
        if status_filter and status_filter != 'all':
            submissions_list = submissions_list.filter(status=status_filter)
            
        # Search
        search_query = request.GET.get('search')
        if search_query:
            submissions_list = submissions_list.filter(
                Q(title__icontains=search_query) | 
                Q(author__username__icontains=search_query)
            )
            
        # Sorting
        sort_by = request.GET.get('sort', 'date_desc')
        if sort_by == 'date_asc':
            submissions_list = submissions_list.order_by('submitted_date')
        elif sort_by == 'title':
            submissions_list = submissions_list.order_by('title')
        else: # date_desc
            submissions_list = submissions_list.order_by('-submitted_date')

        # Pagination
        paginator = Paginator(submissions_list, 10) # 10 items per page
        page = request.GET.get('page')
        try:
            submissions = paginator.page(page)
        except PageNotAnInteger:
            submissions = paginator.page(1)
        except EmptyPage:
            submissions = paginator.page(paginator.num_pages)

        unassigned_count = Manuscript.objects.filter(status='submitted').count()
        total_count = Manuscript.objects.count()
        
        return render(request, 'dashboard/editor_dashboard.html', {
            'submissions': submissions,
            'my_submissions': my_submissions,
            'unassigned_count': unassigned_count,
            'total_count': total_count,
            'current_status': status_filter,
            'current_sort': sort_by,
            'current_search': search_query
        })
    elif request.user.is_reviewer:
        # Get ALL reviews to calculate stats correctly
        all_reviews = Review.objects.filter(reviewer=request.user)
        
        # LAZY SYNC: Ensure reviewer has assignments for the latest rounds 
        # (Fixes cases where revision was submitted before automation was added)
        # Find all manuscripts this reviewer is involved with
        involved_manuscripts = Manuscript.objects.filter(
            reviews__reviewer=request.user, 
            status__in=['revision_submitted', 'under_review', 'needs_revision']
        ).distinct()
        
        for ms in involved_manuscripts:
            latest_rev = all_reviews.filter(manuscript=ms).order_by('-round', '-id').first()
            if latest_rev and ms.current_round > latest_rev.round:
                # Create the missing assignment for the current round
                Review.objects.get_or_create(
                    manuscript=ms,
                    reviewer=request.user,
                    round=ms.current_round,
                    defaults={'invitation_status': 'accepted'}
                )
        
        # Refresh all_reviews after sync
        all_reviews = Review.objects.filter(reviewer=request.user)
        total_reviews = all_reviews.count()
        pending_reviews = all_reviews.filter(date_completed__isnull=True).count()
        completed_reviews = all_reviews.filter(date_completed__isnull=False).count()

        # Consolidate for the "Recent Activity" list: only one entry per (manuscript, round)
        recent_all = all_reviews.order_by('-id')
        seen_keys = set()
        recent_consolidated = []
        for r in recent_all:
            key = (r.manuscript_id, r.round)
            if key not in seen_keys:
                recent_consolidated.append(r)
                seen_keys.add(key)
                if len(recent_consolidated) >= 5:
                    break
        
        return render(request, 'dashboard/reviewer_dashboard.html', {
            'assigned_reviews': recent_consolidated, # Already limited to 5
            'total_reviews': total_reviews,
            'pending_reviews': pending_reviews,
            'completed_reviews': completed_reviews,
        })
    elif request.user.is_researcher:
        # Calculate stats
        total_submissions = my_submissions.count()
        in_review_count = my_submissions.filter(status__in=['submitted', 'under_review', 'needs_revision', 'revision_submitted']).count()
        approved_count = my_submissions.filter(status='accepted').count()
        published_count = my_submissions.filter(status='published').count()
        
        return render(request, 'dashboard/researcher_dashboard.html', {
            'submissions': my_submissions[:5], # Only show recent 5
            'total_submissions': total_submissions,
            'in_review_count': in_review_count,
            'approved_count': approved_count,
            'published_count': published_count,
        })

    else:
        return render(request, 'dashboard/dashboard.html', {
            'my_submissions': my_submissions,
        })

@login_required
def assigned_reviews(request):
    if not request.user.is_reviewer:
        return redirect('dashboard')
        
    # LAZY SYNC: Ensure reviewer has assignments for the latest rounds 
    # (Fixes cases where revision was submitted before automation was added)
    involved_manuscripts = Manuscript.objects.filter(
        reviews__reviewer=request.user, 
        status__in=['revision_submitted', 'under_review', 'needs_revision']
    ).distinct()
    
    for ms in involved_manuscripts:
        latest_rev = Review.objects.filter(reviewer=request.user, manuscript=ms).order_by('-round', '-id').first()
        if latest_rev and ms.current_round > latest_rev.round:
            # Create the missing assignment for the current round
            Review.objects.get_or_create(
                manuscript=ms,
                reviewer=request.user,
                round=ms.current_round,
                defaults={'invitation_status': 'accepted'}
            )

    # Consolidate: only show the LATEST review for each manuscript/round pair
    all_assigned = Review.objects.filter(reviewer=request.user).order_by('-round', '-id')
    seen_keys = set()
    consolidated_reviews = []
    
    for r in all_assigned:
        key = (r.manuscript_id, r.round)
        if key not in seen_keys:
            consolidated_reviews.append(r)
            seen_keys.add(key)
            
    return render(request, 'dashboard/assigned_reviews.html', {
        'assigned_reviews': consolidated_reviews
    })

@login_required
def accept_review_invitation(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    if review.invitation_status == 'invited':
        review.invitation_status = 'accepted'
        review.save()
        messages.success(request, f"You have accepted the invitation to review '{review.manuscript.title}'.")
    return redirect('assigned_reviews')

@login_required
def decline_review_invitation(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    if request.method == 'POST' and review.invitation_status == 'invited':
        reason = request.POST.get('reason')
        review.invitation_status = 'declined'
        review.declined_reason = reason
        review.save()
        messages.info(request, f"You have declined the invitation to review '{review.manuscript.title}'.")
    return redirect('assigned_reviews')

@login_required
def reviewer_check_revision(request, review_id):
    if not request.user.is_reviewer:
        return redirect('dashboard')
    
    old_review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    manuscript = old_review.manuscript
    
    # Security check: Ensure manuscript is in a state that allows checking revision
    if manuscript.status not in ['revision_submitted', 'under_review', 'needs_revision']:
         messages.error(request, "This action is only available for manuscripts currently being revised.")
         return redirect('assigned_reviews')

    if request.method == 'POST':
        form = ReviewForm(request.POST) # NEW record, no instance
        if form.is_valid():
            # Use update_or_create to avoid duplicate records for the same round
            review, created = Review.objects.update_or_create(
                manuscript=manuscript,
                reviewer=request.user,
                round=manuscript.current_round,
                defaults={
                    'recommendation': form.cleaned_data.get('recommendation'),
                    'comments': form.cleaned_data.get('comments'),
                    'invitation_status': 'accepted',
                    'date_completed': timezone.now()
                }
            )
            
            # Notify editors
            for editor in User.objects.filter(is_editor=True):
                Notification.objects.create(
                    recipient=editor,
                    message=f"Follow-up Advice: {request.user.get_full_name()} has submitted updated comments for Round {manuscript.current_round} of '{manuscript.title}'.",
                    link=f'/dashboard/manuscript/{manuscript.id}/'
                )
                
            messages.success(request, "Your follow-up recommendation has been recorded. The editor will be notified.")
            return redirect('reviewer_manuscript_detail', review_id=review.id)
    else:
        # Pre-fill with old review content as a starting point
        form = ReviewForm(initial={
            'recommendation': old_review.recommendation,
            'comments': old_review.comments
        })
    
    return render(request, 'dashboard/submit_review.html', {
        'form': form,
        'manuscript': manuscript,
        'review': old_review, 
        'current_round': manuscript.current_round, # Used for accurate labeling
        'is_locked': False
    })

@login_required
def my_submissions(request):
    submissions_list = Manuscript.objects.filter(author=request.user)
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        submissions_list = submissions_list.filter(status=status_filter)
        
    # Sorting
    sort_by = request.GET.get('sort', 'date_desc')
    if sort_by == 'date_asc':
        submissions_list = submissions_list.order_by('submitted_date')
    elif sort_by == 'title':
        submissions_list = submissions_list.order_by('title')
    else: # date_desc
        submissions_list = submissions_list.order_by('-submitted_date')

    # Pagination
    paginator = Paginator(submissions_list, 10)
    page = request.GET.get('page')
    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        submissions = paginator.page(1)
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)

    return render(request, 'dashboard/my_submissions.html', {
        'submissions': submissions,
        'current_status': status_filter,
        'current_sort': sort_by
    })

@login_required
def reviewer_manuscript_detail(request, review_id):
    # Fetch the specific review requested
    review_assignment = get_object_or_404(Review, id=review_id)
    manuscript = review_assignment.manuscript
    
    # Security check: Ensure this review belongs to the current user
    if review_assignment.reviewer != request.user:
        return redirect('dashboard')
    
    # Proactive Redirect: If this is NOT the latest round assignment, redirect to the latest one
    # Note: We only do this if the user is looking at history; we still want them to be able 
    # to SEE old rounds, but maybe we should clearly distinguish.
    # Actually, the user says they want to see history. I'll just keep them on the page
    # but fix the button issue I already found.
    # Wait, I won't redirect here because "Viewing History" is a valid use case.
    # I'll just ensure the ACTION BUTTONS point to the latest.
    
    # Get all reviews by THIS reviewer for THIS manuscript (history)
    reviewer_history = Review.objects.filter(manuscript=manuscript, reviewer=request.user).order_by('-round', '-id')
    
    # Filter author responses: Show those for the current review round,
    # OR if this is the latest review and a new manuscript round has started, show those too
    if review_assignment.is_latest_round and manuscript.current_round > review_assignment.round:
        author_responses = manuscript.author_responses.filter(round__in=[review_assignment.round, manuscript.current_round]).order_by('-round', '-id')
    else:
        author_responses = manuscript.author_responses.filter(round=review_assignment.round).order_by('-id')
        
    return render(request, 'dashboard/reviewer_manuscript_detail.html', {
        'manuscript': manuscript,
        'review': review_assignment,
        'reviewer_history': reviewer_history,
        'author_responses': author_responses
    })

@login_required
def my_submission_detail(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    
    # Security check: Ensure user owns this manuscript
    if manuscript.author != request.user:
        return redirect('my_submissions')
        
    # Get all responses by this author for this manuscript
    author_responses = manuscript.author_responses.all().order_by('-round', '-id')
        
    return render(request, 'dashboard/my_submission_detail.html', {
        'manuscript': manuscript,
        'author_responses': author_responses
    })

@login_required
@verified_email_required
def submit_manuscript(request):
    if request.method == 'POST':
        form = ManuscriptForm(request.POST, request.FILES)
        if form.is_valid():
            manuscript = form.save(commit=False)
            manuscript.author = request.user
            manuscript.save()
            
            # Send Email to Author
            dashboard_url = request.build_absolute_uri(reverse('dashboard'))
            author_context = {
                'author_name': manuscript.author.get_full_name() or manuscript.author.username,
                'title': manuscript.title,
                'dashboard_url': dashboard_url
            }
            author_html = render_to_string('emails/manuscript_submitted_author.html', author_context)
            _send_notification_email(
                f"Submission Received: {manuscript.title}",
                f"Your manuscript '{manuscript.title}' has been successfully submitted.",
                [manuscript.author.email],
                html_message=author_html
            )
            
            # Send Email to Editors
            editor_emails = list(User.objects.filter(is_editor=True).values_list('email', flat=True))
            if editor_emails:
                editor_context = {
                    'author_name': manuscript.author.get_full_name() or manuscript.author.username,
                    'title': manuscript.title,
                    'dashboard_url': dashboard_url
                }
                editor_html = render_to_string('emails/manuscript_submitted_editor.html', editor_context)
                _send_notification_email(
                    f"New Submission: {manuscript.title}",
                    f"A new manuscript '{manuscript.title}' has been submitted.",
                    editor_emails,
                    html_message=editor_html
                )
            
            messages.success(request, "Your manuscript has been submitted successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below and try again.")
    else:
        form = ManuscriptForm()
    return render(request, 'dashboard/submit_manuscript.html', {'form': form})

@login_required
def assign_reviewer(request, manuscript_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    
    # Get all reviews for this manuscript
    existing_reviews = Review.objects.filter(manuscript=manuscript)
    active_reviewer_ids = existing_reviews.exclude(invitation_status='declined').values_list('reviewer_id', flat=True)
    
    if request.method == 'POST':
        reviewer_id = request.POST.get('reviewer')
        if reviewer_id:
            reviewer = get_object_or_404(User, id=reviewer_id)
            
            # Check if active assignment already exists
            if not Review.objects.filter(manuscript=manuscript, reviewer=reviewer).exclude(invitation_status='declined').exists():
                # Get due date from form or default to 14 days
                due_date_str = request.POST.get('due_date')
                if due_date_str:
                    due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%d').date()
                else:
                    due_date = timezone.now().date() + timezone.timedelta(days=14)
                
                # Check for invitation status
                invite_only = request.POST.get('invite_only') == 'on'
                status = 'invited' if invite_only else 'assigned'
                
                # Check if we are reactivating a declined review or creating a new one
                declined_review = Review.objects.filter(manuscript=manuscript, reviewer=reviewer, invitation_status='declined').first()
                if declined_review:
                    declined_review.invitation_status = status
                    declined_review.due_date = due_date
                    declined_review.round = manuscript.current_round
                    declined_review.declined_reason = ''  # clear old reason
                    declined_review.save()
                else:
                    Review.objects.create(
                        manuscript=manuscript, 
                        reviewer=reviewer, 
                        due_date=due_date,
                        round=manuscript.current_round,
                        invitation_status=status
                    )
                
                # Send Email to Reviewer
                dashboard_url = request.build_absolute_uri(reverse('dashboard'))
                reviewer_context = {
                    'reviewer_name': reviewer.get_full_name() or reviewer.username,
                    'title': manuscript.title,
                    'dashboard_url': dashboard_url
                }
                reviewer_html = render_to_string('emails/reviewer_assigned.html', reviewer_context)
                _send_notification_email(
                    f"New Review Assignment: {manuscript.title}",
                    f"You have been assigned to review '{manuscript.title}'.",
                    [reviewer.email],
                    html_message=reviewer_html
                )
                
                msg = f"Reviewer {reviewer.username} invited successfully." if invite_only else f"Reviewer {reviewer.username} assigned successfully."
                messages.success(request, msg)
                return redirect('dashboard')
    
    # Filter out reviewers who are already ACTIVELY assigned
    reviewers = User.objects.filter(is_reviewer=True).exclude(id__in=active_reviewer_ids)
    
    return render(request, 'dashboard/assign_reviewer.html', {
        'manuscript': manuscript, 
        'reviewers': reviewers, 
        'existing_reviews': existing_reviews
    })

@login_required
def submit_review(request, review_id):
    # Fetch the specific review requested
    review = get_object_or_404(Review, id=review_id)
    manuscript = review.manuscript
    
    # Security check: Ensure this review belongs to the current user
    if review.reviewer != request.user:
        return redirect('dashboard')
    
    # Check if this review can be edited (locked if already published OR not the latest round)
    is_locked = manuscript.status == 'published' or not review.is_latest_round
    
    if request.method == 'POST':
        if is_locked:
            messages.error(request, "This review is locked and cannot be edited.")
            latest_assignment = manuscript.reviews.filter(reviewer=request.user).order_by('-round', '-id').first()
            return redirect('reviewer_manuscript_detail', review_id=latest_assignment.id)
            
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.date_completed = timezone.now()
            review.save()
            
            # Notify editors that a review has been submitted/updated
            for editor in User.objects.filter(is_editor=True):
                Notification.objects.create(
                    recipient=editor,
                    message=f"Review Submitted: {request.user.get_full_name()} has submitted their assessment for Round {review.round} of '{manuscript.title}'.",
                    link=f'/dashboard/manuscript/{manuscript.id}/'
                )
                
            messages.success(request, "Your assessment has been submitted. Thank you!")
            return redirect('dashboard')
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'dashboard/submit_review.html', {
        'form': form, 
        'manuscript': manuscript,
        'is_locked': is_locked,
        'review': review
    })

@login_required
def request_re_review(request, review_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    old_review = get_object_or_404(Review, id=review_id)
    manuscript = old_review.manuscript
    
    # Create a NEW review for the next round
    new_round = old_review.round + 1
    
    # Check if a review for this round already exists to avoid duplicates
    if not Review.objects.filter(manuscript=manuscript, reviewer=old_review.reviewer, round=new_round).exists():
        Review.objects.create(
            manuscript=manuscript,
            reviewer=old_review.reviewer,
            round=new_round,
            due_date=(timezone.now() + timezone.timedelta(days=7)).date()
        )
        
        # Also update manuscript status back to under_review if needed
        if manuscript.status == 'revision_submitted':
            manuscript.status = 'under_review'
            manuscript.save()
            
        messages.success(request, f"Round {new_round} review requested from {old_review.reviewer.username}.")
    else:
        messages.info(request, f"Round {new_round} review already requested for this reviewer.")

    return redirect('dashboard_manuscript_detail', manuscript_id=manuscript.id)

@login_required
def accept_review_invitation(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    referer = request.META.get('HTTP_REFERER') or 'assigned_reviews'
    
    if review.invitation_status != 'invited':
        messages.error(request, "This invitation has already been responded to.")
        return redirect(referer)
    
    review.invitation_status = 'accepted'
    review.save()
    
    # Notify editors
    for editor in User.objects.filter(is_editor=True):
        Notification.objects.create(
            recipient=editor,
            message=f"Invitation Accepted: {request.user.username} has accepted the review invitation for '{review.manuscript.title}'.",
            link=f'/dashboard/manuscript/{review.manuscript.id}/'
        )
    
    messages.success(request, f"You have accepted the review invitation for '{review.manuscript.title}'.")
    return redirect(referer)

@login_required
def decline_review_invitation(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    referer = request.META.get('HTTP_REFERER') or 'assigned_reviews'
    
    if review.invitation_status != 'invited':
        messages.error(request, "This invitation has already been responded to.")
        return redirect(referer)
    
    if request.method == 'POST':
        review.invitation_status = 'declined'
        review.declined_reason = request.POST.get('reason', '')
        review.save()
        
        # Notify editors
        for editor in User.objects.filter(is_editor=True):
            Notification.objects.create(
                recipient=editor,
                message=f"Invitation Declined: {request.user.username} has declined the review invitation for '{review.manuscript.title}'.",
                link=f'/dashboard/manuscript/{review.manuscript.id}/'
            )
        
        messages.success(request, f"You have declined the review invitation for '{review.manuscript.title}'.")
        return redirect(referer)
    
    return redirect(referer)

@login_required
def reviewer_check_revision(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    return redirect('reviewer_manuscript_detail', review_id=review.id)

@login_required
def make_decision(request, manuscript_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    if request.method == 'POST':
        decision = request.POST.get('decision')
        if decision in ['accepted', 'rejected', 'needs_revision']:
            manuscript.status = decision
            if decision == 'needs_revision':
                manuscript.current_round += 1
            manuscript.status_changed = True
            manuscript.save()
            
            if decision == 'needs_revision':
                # Push all completed reviews to author visibility
                manuscript.reviews.filter(date_completed__isnull=False).update(is_visible_to_author=True)
                
                # Send Email to Author
                dashboard_url = request.build_absolute_uri(reverse('dashboard'))
                author_context = {
                    'author_name': manuscript.author.get_full_name() or manuscript.author.username,
                    'title': manuscript.title,
                    'dashboard_url': dashboard_url
                }
                author_html = render_to_string('emails/revision_requested.html', author_context)
                _send_notification_email(
                    f"Revision Required: {manuscript.title}",
                    f"A revision has been requested for your manuscript '{manuscript.title}'.",
                    [manuscript.author.email],
                    html_message=author_html
                )
            
            messages.success(request, f"Decision '{decision}' recorded for {manuscript.title}.")
        return redirect('dashboard')
    
    reviews = manuscript.reviews.filter(date_completed__isnull=False).order_by('-round', '-id')
    author_responses = manuscript.author_responses.all().order_by('-round', '-id')
    return render(request, 'dashboard/make_decision.html', {'manuscript': manuscript, 'reviews': reviews, 'author_responses': author_responses})

@login_required
@verified_email_required
def submit_revision(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id, author=request.user)
    
    if manuscript.status != 'needs_revision':
        messages.error(request, "This manuscript does not require a revision at this time.")
        return redirect('my_submission_detail', manuscript_id=manuscript.id)
        
    if request.method == 'POST':
        form = RevisionForm(request.POST, request.FILES, instance=manuscript)
        if form.is_valid():
            manuscript = form.save(commit=False)
            manuscript.status = 'revision_submitted'
            manuscript.status_changed = True
            manuscript.save()

            # Save historical author response
            from .models import AuthorResponse
            AuthorResponse.objects.create(
                manuscript=manuscript,
                round=manuscript.current_round,
                content=form.cleaned_data.get('response_to_reviewers')
            )

            # AUTOMATION: Create new review records for the NEXT round for all existing reviewers
            # This ensures the new round appears as a fresh activity on their dashboards
            previous_reviewers = Review.objects.filter(manuscript=manuscript).values_list('reviewer_id', flat=True).distinct()
            reviewer_emails = []
            for rev_id in previous_reviewers:
                # Only create if doesn't exist for this exact round
                Review.objects.get_or_create(
                    manuscript=manuscript,
                    reviewer_id=rev_id,
                    round=manuscript.current_round,
                    defaults={'invitation_status': 'accepted'}
                )
                try:
                    reviewer = User.objects.get(id=rev_id)
                    reviewer_emails.append(reviewer.email)
                except User.DoesNotExist:
                    pass
            
            dashboard_url = request.build_absolute_uri(reverse('dashboard'))
            
            # Send Email to Reviewers
            if reviewer_emails:
                rev_context = {
                    'reviewer_name': 'Reviewer',
                    'title': manuscript.title,
                    'dashboard_url': dashboard_url
                }
                rev_html = render_to_string('emails/revision_submitted_reviewer.html', rev_context)
                _send_notification_email(
                    f"Manuscript Revision Submitted: {manuscript.title}",
                    f"A revision has been submitted for '{manuscript.title}'.",
                    reviewer_emails,
                    html_message=rev_html
                )
            
            # Send Email to Editors
            editor_emails = list(User.objects.filter(is_editor=True).values_list('email', flat=True))
            if editor_emails:
                editor_context = {
                    'author_name': manuscript.author.get_full_name() or manuscript.author.username,
                    'title': manuscript.title,
                    'dashboard_url': dashboard_url
                }
                editor_html = render_to_string('emails/revision_submitted_editor.html', editor_context)
                _send_notification_email(
                    f"Manuscript Revision Submitted: {manuscript.title}",
                    f"A revision has been submitted for '{manuscript.title}'.",
                    editor_emails,
                    html_message=editor_html
                )

            messages.success(request, "Your revision has been submitted successfully.")
            return redirect('my_submission_detail', manuscript_id=manuscript.id)
    else:
        form = RevisionForm(instance=manuscript)
        
    return render(request, 'dashboard/submit_revision.html', {
        'form': form, 
        'manuscript': manuscript
    })

@login_required
def mark_as_paid(request, manuscript_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    manuscript.is_paid = True
    manuscript.save()
    
    _send_notification_email(
        f"Payment Confirmed: {manuscript.title}",
        f"Dear {manuscript.author.get_full_name()},\n\nWe have confirmed your payment for the manuscript '{manuscript.title}'.\nYour manuscript is now ready for publication.\n\nBest regards,\nJHST Editorial Team",
        [manuscript.author.email]
    )

    Notification.objects.create(
        recipient=manuscript.author,
        message=f"Payment Confirmed: Your payment for '{manuscript.title}' has been verified.",
        link='/dashboard/my-submissions/'
    )
    
    messages.success(request, f"Payment confirmed for {manuscript.title}.")
    return redirect('dashboard')

@login_required
def publish_article(request, manuscript_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    
    # Payment check removed to allow publishing before payment as per user request
    # if not manuscript.is_paid: ...

    if request.method == 'POST':
        issue_id = request.POST.get('issue')
        issue = get_object_or_404(Issue, id=issue_id)
        
        page_start = request.POST.get('page_start')
        page_end = request.POST.get('page_end')
        doi = request.POST.get('doi')
        
        Article.objects.create(
            manuscript=manuscript, 
            issue=issue,
            page_start=page_start if page_start else None,
            page_end=page_end if page_end else None,
            doi=doi if doi else None
        )

        # Update manuscript status
        manuscript.status = 'published'
        manuscript.status_changed = True
        manuscript.save()
        
        # Send Email to Author
        article_url = request.build_absolute_uri(reverse('article_detail', args=[manuscript.article.id]))
        author_context = {
            'author_name': manuscript.author.get_full_name() or manuscript.author.username,
            'title': manuscript.title,
            'article_url': article_url
        }
        author_html = render_to_string('emails/article_published.html', author_context)
        _send_notification_email(
            f"Article Published: {manuscript.title}",
            f"Your manuscript '{manuscript.title}' has been successfully published.",
            [manuscript.author.email],
            html_message=author_html
        )

        messages.success(request, f"Article published to {issue} successfully.")
        return redirect('dashboard')
    
    issues = Issue.objects.all()
    return render(request, 'dashboard/publish_article.html', {'manuscript': manuscript, 'issues': issues})

@login_required
def dashboard_manuscript_detail(request, manuscript_id):
    if not request.user.is_editor: # Restrict to editor for now as per "action buttons" context
        return redirect('dashboard')
    
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    reviews = manuscript.reviews.all().order_by('-round', '-id')
    author_responses = manuscript.author_responses.all().order_by('-round', '-id')
    
    return render(request, 'dashboard/manuscript_detail.html', {
        'manuscript': manuscript,
        'reviews': reviews,
        'author_responses': author_responses,
    })

@login_required
def create_issue(request):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save()
            messages.success(request, f"Issue {issue} created successfully.")
            return redirect('dashboard')
    else:
        form = IssueForm()
    return render(request, 'dashboard/create_issue.html', {'form': form})

@login_required
def create_volume(request):
    if not request.user.is_editor:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = VolumeForm(request.POST)
        if form.is_valid():
            volume = form.save()
            messages.success(request, f"Volume {volume} created successfully.")
            return redirect('create_issue') # Redirect to issue creation as natural next step
    else:
        form = VolumeForm()
    return render(request, 'dashboard/create_volume.html', {'form': form})

@login_required
def manage_volumes(request):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    volumes = Volume.objects.prefetch_related('issues__articles').order_by('-year', '-number')
    return render(request, 'dashboard/manage_volumes.html', {'volumes': volumes})

@login_required
def manage_issue(request, issue_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    issue = get_object_or_404(Issue, id=issue_id)
    return render(request, 'dashboard/manage_issue.html', {'issue': issue})

def index(request):
    latest_issues = Issue.objects.all().order_by('-publication_date')[:5]
    return render(request, 'journal/index.html', {'latest_issues': latest_issues})

def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    return render(request, 'journal/issue_detail.html', {'issue': issue})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'journal/article_detail.html', {'article': article})

def search(request):
    query = request.GET.get('q', '')
    author_query = request.GET.get('author', '')
    year_query = request.GET.get('year', '')
    
    results = Article.objects.all()
    has_filters = False

    if query:
        has_filters = True
        results = results.filter(
            Q(manuscript__title__icontains=query) | 
            Q(manuscript__abstract__icontains=query) |
            Q(manuscript__keywords__icontains=query)
        )
        
    if author_query:
        has_filters = True
        results = results.filter(
            Q(manuscript__author__username__icontains=author_query) |
            Q(manuscript__author__first_name__icontains=author_query) |
            Q(manuscript__author__last_name__icontains=author_query) |
            Q(manuscript__co_authors__icontains=author_query)
        )
        
    if year_query and year_query.isdigit():
        has_filters = True
        results = results.filter(issue__volume__year=int(year_query))

    if not has_filters:
        results = []

    return render(request, 'journal/search_results.html', {
        'results': results, 
        'query': query,
        'author_query': author_query,
        'year_query': year_query
    })
def archives(request):
    volumes = Volume.objects.prefetch_related('issues').order_by('-year', '-number')
    return render(request, 'journal/archives.html', {'volumes': volumes})

def current_issue(request):
    issue = Issue.objects.order_by('-publication_date').first()
    return render(request, 'journal/current_issue.html', {'issue': issue})

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def announcements(request):
    announcements_list = Announcement.objects.filter(is_active=True).order_by('-date_created')
    
    # Pagination
    paginator = Paginator(announcements_list, 5) # 5 per page
    page = request.GET.get('page')
    try:
        announcements = paginator.page(page)
    except PageNotAnInteger:
        announcements = paginator.page(1)
    except EmptyPage:
        announcements = paginator.page(paginator.num_pages)
        
    return render(request, 'journal/announcements.html', {'announcements': announcements})

def announcement_detail(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    return render(request, 'journal/announcement_detail.html', {'announcement': announcement})

@login_required
def resend_verification_email(request):
    user = request.user
    if user.is_email_verified:
        messages.info(request, "Your email is already verified.")
        return redirect('dashboard')
        
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )
    
    html_message = render_to_string('emails/verify_email.html', {
        'user': user,
        'verification_url': verification_url
    })
    text_message = render_to_string('emails/verify_email.txt', {
        'user': user,
        'verification_url': verification_url
    })
    
    try:
        sender = getattr(settings, 'EMAIL_HOST_USER', 'noreply@jhst.org')
        send_mail(
            subject="Verify your JHST account",
            message=text_message,
            from_email=sender,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
        messages.success(request, "Verification email has been resent. Please check your inbox.")
    except Exception as e:
        messages.error(request, "There was a problem sending the verification email. Please try again later.")
        print(f"Error sending email: {e}")
        
    return redirect('dashboard')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.success(request, "Your email address has been successfully verified! You now have full access to all features.")
        if not request.user.is_authenticated:
            login(request, user)
        return redirect('dashboard')
    else:
        messages.error(request, "The verification link was invalid or has expired. Please request a new one.")
        return redirect('dashboard')
