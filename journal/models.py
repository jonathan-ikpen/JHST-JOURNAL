from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    is_researcher = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    affiliation = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

class Manuscript(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    abstract = models.TextField()
    file = models.FileField(upload_to='manuscripts/')
    co_authors = models.CharField(max_length=500, blank=True, help_text="Names of co-authors, separated by commas")
    affiliations = models.TextField(blank=True, help_text="Author affiliations")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manuscripts')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_manuscripts')
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords")
    is_paid = models.BooleanField(default=False, help_text="Has the publication fee been paid?")

    def __str__(self):
        return self.title

    @property
    def progress_width_class(self):
        if self.status == 'submitted':
            return 'w-1/3'
        elif self.status == 'under_review':
            return 'w-2/3'
        elif self.status in ['accepted', 'rejected', 'published']:
            return 'w-full'
        return 'w-0'

    @property
    def progress_color_class(self):
        if self.status == 'rejected':
            return 'bg-red-500'
        return 'bg-primary'

class Review(models.Model):
    RECOMMENDATION_CHOICES = [
        ('accept', 'Accept'),
        ('revise', 'Revise'),
        ('reject', 'Reject'),
    ]

    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    date_assigned = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATION_CHOICES, blank=True)

    def __str__(self):
        return f"Review of {self.manuscript.title} by {self.reviewer.username}"

class Volume(models.Model):
    number = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"Vol {self.number} ({self.year})"

class Issue(models.Model):
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, related_name='issues')
    number = models.IntegerField()
    publication_date = models.DateField()

    def __str__(self):
        return f"Vol {self.volume.number}, Issue {self.number}"

class Article(models.Model):
    manuscript = models.OneToOneField(Manuscript, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='articles')
    page_start = models.IntegerField(null=True, blank=True)
    page_end = models.IntegerField(null=True, blank=True)
    doi = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.manuscript.title

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"
