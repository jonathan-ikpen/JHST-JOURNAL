from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ResearcherRegistrationForm, ManuscriptForm, ReviewForm, VolumeForm, IssueForm, UserProfileForm
from .models import Manuscript, Review, User, Issue, Article, Volume, Notification, Announcement, Page

def cms_page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, page.template_name, {'page': page})

def _send_notification_email(subject, message, recipient_list):
    """
    Helper function to send emails without blocking.
    Prints error to console if fails (development mode).
    """
    try:
        # If EMAIL_HOST_USER is not set, use a dummy sender
        sender = getattr(settings, 'EMAIL_HOST_USER', 'noreply@jhst.org')
        send_mail(subject, message, sender, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Error sending email: {e}")


def register(request):
    if request.method == 'POST':
        form = ResearcherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to JHST, {user.username}! Your account has been created.")
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
            'notifications': Notification.objects.filter(recipient=request.user, is_read=False)[:5],
            'current_status': status_filter,
            'current_sort': sort_by,
            'current_search': search_query
        })
    elif request.user.is_reviewer:
        # Check if user is a reviewer
        assigned_reviews = Review.objects.filter(reviewer=request.user).order_by('-date_assigned')
        
        # Calculate stats
        total_reviews = assigned_reviews.count()
        pending_reviews = assigned_reviews.filter(date_completed__isnull=True).count()
        completed_reviews = assigned_reviews.filter(date_completed__isnull=False).count()
        
        return render(request, 'dashboard/reviewer_dashboard.html', {
            'assigned_reviews': assigned_reviews[:5], # Recent activity
            'total_reviews': total_reviews,
            'pending_reviews': pending_reviews,
            'completed_reviews': completed_reviews,
            'notifications': Notification.objects.filter(recipient=request.user, is_read=False)[:5]
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
            'notifications': Notification.objects.filter(recipient=request.user, is_read=False)[:5]
        })

    else:
        return render(request, 'dashboard/dashboard.html', {
            'my_submissions': my_submissions,
            'notifications': Notification.objects.filter(recipient=request.user, is_read=False)[:5]
        })

@login_required
def assigned_reviews(request):
    if not request.user.is_reviewer:
        return redirect('dashboard')
        
    assigned_reviews = Review.objects.filter(reviewer=request.user).order_by('-round', '-date_assigned')
    return render(request, 'dashboard/assigned_reviews.html', {
        'assigned_reviews': assigned_reviews
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
    
    # Get all reviews by THIS reviewer for THIS manuscript (history)
    reviewer_history = Review.objects.filter(manuscript=manuscript, reviewer=request.user).order_by('round')
        
    return render(request, 'dashboard/reviewer_manuscript_detail.html', {
        'manuscript': manuscript,
        'review': review_assignment,
        'reviewer_history': reviewer_history
    })

@login_required
def my_submission_detail(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    
    # Security check: Ensure user owns this manuscript
    if manuscript.author != request.user:
        return redirect('my_submissions')
        
    return render(request, 'dashboard/my_submission_detail.html', {
        'manuscript': manuscript
    })

@login_required
def submit_manuscript(request):
    if request.method == 'POST':
        form = ManuscriptForm(request.POST, request.FILES)
        if form.is_valid():
            manuscript = form.save(commit=False)
            manuscript.author = request.user
            manuscript.save()
            
            # Send notification to author
            _send_notification_email(
                f"Submission Received: {manuscript.title}",
                f"Dear {manuscript.author.get_full_name()},\n\nYour manuscript '{manuscript.title}' has been successfully submitted to JHST. You can track its status in your dashboard.\n\nBest regards,\nJHST Editorial Team",
                [manuscript.author.email]
            )
            
            # In-app notification for Author
            Notification.objects.create(
                recipient=manuscript.author,
                message=f"Submission Received: Your manuscript '{manuscript.title}' has been successfully submitted.",
                link='/dashboard/my-submissions/'
            )
            
            # Notify Editors
            for editor in User.objects.filter(is_editor=True):
                 Notification.objects.create(
                    recipient=editor,
                    message=f"New Submission: '{manuscript.title}' by {manuscript.author.get_full_name()}.",
                    link='/dashboard/'
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
    
    # Get all reviews for this manuscript to see who is already assigned
    existing_reviews = Review.objects.filter(manuscript=manuscript)
    assigned_reviewer_ids = existing_reviews.values_list('reviewer_id', flat=True)
    
    if request.method == 'POST':
        reviewer_id = request.POST.get('reviewer')
        if reviewer_id:
            reviewer = get_object_or_404(User, id=reviewer_id)
            
            # Check if already assigned
            if not Review.objects.filter(manuscript=manuscript, reviewer=reviewer).exists():
                # Get due date from form or default to 14 days
                due_date_str = request.POST.get('due_date')
                if due_date_str:
                    due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%d').date()
                else:
                    due_date = timezone.now().date() + timezone.timedelta(days=14)
                
                Review.objects.create(manuscript=manuscript, reviewer=reviewer, due_date=due_date)
                messages.success(request, f"Reviewer {reviewer.username} assigned successfully.")
                return redirect('dashboard')
    
    # Filter out reviewers who are already assigned
    reviewers = User.objects.filter(is_reviewer=True).exclude(id__in=assigned_reviewer_ids)
    
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
            return redirect('reviewer_manuscript_detail', review_id=review.id)
            
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.date_completed = timezone.now()
            review.save()
            messages.success(request, "Your review has been submitted. Thank you!")
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
def make_decision(request, manuscript_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    if request.method == 'POST':
        decision = request.POST.get('decision')
        if decision in ['accepted', 'rejected', 'needs_revision']:
            manuscript.status = decision
            manuscript.save()
            
            if decision == 'needs_revision':
                # Push all completed reviews to author visibility
                manuscript.reviews.filter(date_completed__isnull=False).update(is_visible_to_author=True)
            
            # Notify Author (Decision notification is mostly handled by signals now, 
            # but let's keep the existing logic or adapt it)
            # Actually, signals handle needs_revision. accepted/rejected still here?
            # Let's keep accepted/rejected here for now since they are not in signals yet.
            if decision in ['accepted', 'rejected']:
                _send_notification_email(
                    f"Decision on Manuscript: {manuscript.title}",
                    f"Dear {manuscript.author.get_full_name()},\n\nA decision has been reached regarding your manuscript '{manuscript.title}': {decision.upper()}.\nPlease log in to your dashboard to view details and reviews.\n\nIMPORTANT: If your manuscript has been accepted, please proceed to pay the publication fee. Instructions can be found here: {request.build_absolute_uri('/about/publication-fees/')}\n\nBest regards,\nJHST Editorial Team",
                    [manuscript.author.email]
                )

                # In-app notification for Author
                Notification.objects.create(
                    recipient=manuscript.author,
                    message=f"Decision Reached: Your manuscript '{manuscript.title}' has been {decision.upper()}.",
                    link='/dashboard/my-submissions/'
                )
            
            messages.success(request, f"Decision '{decision}' recorded for {manuscript.title}.")
        return redirect('dashboard')
    
    reviews = manuscript.reviews.filter(date_completed__isnull=False).order_by('-round')
    return render(request, 'dashboard/make_decision.html', {'manuscript': manuscript, 'reviews': reviews})

@login_required
def submit_revision(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id, author=request.user)
    
    if manuscript.status != 'needs_revision':
        messages.error(request, "This manuscript does not require a revision at this time.")
        return redirect('my_submission_detail', manuscript_id=manuscript.id)
        
    if request.method == 'POST':
        form = ManuscriptForm(request.POST, request.FILES, instance=manuscript)
        if form.is_valid():
            manuscript = form.save(commit=False)
            manuscript.status = 'revision_submitted'
            manuscript.save()
            messages.success(request, "Your revision has been submitted successfully.")
            return redirect('my_submission_detail', manuscript_id=manuscript.id)
    else:
        form = ManuscriptForm(instance=manuscript)
        
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
        manuscript.save()

        # Notify Author
        _send_notification_email(
            f"Manuscript Published: {manuscript.title}",
            f"Dear {manuscript.author.get_full_name()},\n\nWe are pleased to inform you that your manuscript '{manuscript.title}' has been published in {issue}.\nYou can view it here: {request.build_absolute_uri(f'/article/{Article.objects.get(manuscript=manuscript).id}/')}\n\nCongratulations!\nJHST Editorial Team",
            [manuscript.author.email]
        )

        # In-app notification for Author
        Notification.objects.create(
            recipient=manuscript.author,
            message=f"Published: Your manuscript '{manuscript.title}' is now published in {issue}.",
            link=f"/article/{Article.objects.get(manuscript=manuscript).id}/"
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
    reviews = manuscript.reviews.all().order_by('-round')
    
    return render(request, 'dashboard/manuscript_detail.html', {
        'manuscript': manuscript,
        'reviews': reviews,
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
    home_page = Page.objects.filter(slug='home').first()
    return render(request, 'journal/index.html', {
        'latest_issues': latest_issues,
        'page': home_page
    })

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

