from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .forms import ResearcherRegistrationForm, ManuscriptForm, ReviewForm
from .models import Manuscript, Review, User, Issue, Article

def register(request):
    if request.method == 'POST':
        form = ResearcherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = ResearcherRegistrationForm()
    return render(request, 'journal/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_researcher:
        submissions = Manuscript.objects.filter(author=request.user)
        return render(request, 'journal/researcher_dashboard.html', {'submissions': submissions})
    elif request.user.is_editor:
        submissions = Manuscript.objects.all().order_by('-submitted_date')
        return render(request, 'journal/editor_dashboard.html', {'submissions': submissions})
    elif request.user.is_reviewer:
        assigned_manuscripts = Manuscript.objects.filter(reviewer=request.user)
        return render(request, 'journal/reviewer_dashboard.html', {'assigned_manuscripts': assigned_manuscripts})
    else:
        return render(request, 'journal/dashboard.html')

@login_required
def submit_manuscript(request):
    if request.method == 'POST':
        form = ManuscriptForm(request.POST, request.FILES)
        if form.is_valid():
            manuscript = form.save(commit=False)
            manuscript.author = request.user
            manuscript.save()
            return redirect('dashboard')
    else:
        form = ManuscriptForm()
    return render(request, 'journal/submit_manuscript.html', {'form': form})

@login_required
def assign_reviewer(request, manuscript_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    if request.method == 'POST':
        reviewer_id = request.POST.get('reviewer')
        reviewer = get_object_or_404(User, id=reviewer_id)
        manuscript.reviewer = reviewer
        manuscript.status = 'under_review'
        manuscript.save()
        return redirect('dashboard')
    
    reviewers = User.objects.filter(is_reviewer=True)
    return render(request, 'journal/assign_reviewer.html', {'manuscript': manuscript, 'reviewers': reviewers})

@login_required
def submit_review(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id, reviewer=request.user)
    
    # Check if a review already exists for this manuscript and reviewer
    review, created = Review.objects.get_or_create(manuscript=manuscript, reviewer=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.date_completed = timezone.now()
            review.save()
            return redirect('dashboard')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'journal/submit_review.html', {'form': form, 'manuscript': manuscript})

@login_required
def make_decision(request, manuscript_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    if request.method == 'POST':
        decision = request.POST.get('decision')
        if decision in ['accepted', 'rejected']:
            manuscript.status = decision
            manuscript.save()
        return redirect('dashboard')
    
    reviews = manuscript.reviews.all()
    return render(request, 'journal/make_decision.html', {'manuscript': manuscript, 'reviews': reviews})

@login_required
def publish_article(request, manuscript_id):
    if not request.user.is_editor:
        return redirect('dashboard')
    
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    if request.method == 'POST':
        issue_id = request.POST.get('issue')
        issue = get_object_or_404(Issue, id=issue_id)
        Article.objects.create(manuscript=manuscript, issue=issue)
        return redirect('dashboard')
    
    issues = Issue.objects.all()
    return render(request, 'journal/publish_article.html', {'manuscript': manuscript, 'issues': issues})

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
    query = request.GET.get('q')
    results = []
    if query:
        results = Article.objects.filter(
            Q(manuscript__title__icontains=query) | 
            Q(manuscript__abstract__icontains=query) |
            Q(manuscript__keywords__icontains=query) |
            Q(manuscript__author__username__icontains=query) |
            Q(manuscript__author__first_name__icontains=query) |
            Q(manuscript__author__last_name__icontains=query)
        )
    return render(request, 'journal/search_results.html', {'results': results, 'query': query})
