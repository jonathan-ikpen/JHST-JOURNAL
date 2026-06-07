from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from ckeditor.fields import RichTextField

class User(AbstractUser):
    is_researcher = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    affiliation = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    orcid = models.CharField(max_length=19, blank=True, null=True, help_text="Format: XXXX-XXXX-XXXX-XXXX")

    def __str__(self):
        return self.username

class Manuscript(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('needs_revision', 'Needs Revision'),
        ('revision_submitted', 'Revision Submitted'),
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
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords")
    is_paid = models.BooleanField(default=False, help_text="Has the publication fee been paid?")
    response_to_reviewers = models.TextField(blank=True, help_text="Author's response to reviewer concerns")
    current_round = models.PositiveIntegerField(default=1, help_text="The current version/cycle identifier")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_status = self.status

    @property
    def visible_reviews(self):
        return self.reviews.filter(is_visible_to_author=True).order_by('-round', '-id')

    def save(self, *args, **kwargs):
        self.status_changed = self.status != self._initial_status
        super().save(*args, **kwargs)
        self._initial_status = self.status

    def __str__(self):
        return self.title

    @property
    def progress_width_class(self):
        if self.status == 'submitted':
            return 'w-1/4'
        elif self.status == 'under_review':
            return 'w-2/4'
        elif self.status == 'needs_revision':
            return 'w-3/4'
        elif self.status == 'revision_submitted':
            return 'w-3/4'
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
    is_visible_to_author = models.BooleanField(default=False)
    round = models.PositiveIntegerField(default=1)
    
    INVITATION_STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('invited', 'Invited'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    invitation_status = models.CharField(max_length=20, choices=INVITATION_STATUS_CHOICES, default='assigned')
    declined_reason = models.TextField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_date_completed = self.date_completed

    def save(self, *args, **kwargs):
        self.date_completed_changed = self.date_completed != self._initial_date_completed
        super().save(*args, **kwargs)
        self._initial_date_completed = self.date_completed

    @property
    def has_next_round(self):
        return Review.objects.filter(
            manuscript=self.manuscript,
            reviewer=self.reviewer,
            round=self.round + 1
        ).exists()

    @property
    def has_unreviewed_revision(self):
        """Returns True if there is a revision submitted after this review was completed.
           Excludes history if a subsequent review record already exists."""
        if not self.date_completed or self.has_next_round:
            return False
            
        latest_response = self.manuscript.author_responses.order_by('-date_submitted').first()
        if not latest_response:
            return False
            
        # If response is for a NEWER round, it's definitely unreviewed
        if latest_response.round > self.round:
            return True
            
        # If same round, compare timestamps
        return latest_response.date_submitted > self.date_completed

    @property
    def is_latest_round(self):
        # Use _id fields to avoid triggering full object instantiation or recursive property lookups
        # With multiple follow-ups per round, the "latest" is the one with the highest ID
        from django.db.models import Max
        res = self.__class__.objects.filter(
            manuscript_id=self.manuscript_id, 
            reviewer_id=self.reviewer_id
        ).aggregate(max_id=Max('id'))
        return self.id == res['max_id']

    @property
    def is_awaiting_author(self):
        """Returns True if this is a pending round (2+) where the author hasn't submitted their revision yet."""
        if self.date_completed:
            return False
        # Round 1 is the initial assignment — nothing to await from the author
        if self.round <= 1:
            return False
        # For Round 2+, check if an author response exists for this round yet
        return not self.manuscript.author_responses.filter(round=self.round).exists()

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

class AuthorResponse(models.Model):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='author_responses')
    round = models.PositiveIntegerField()
    content = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-round']

    def __str__(self):
        return f"Response for {self.manuscript.title} - Round {self.round}"

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

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('call_for_papers', 'Call for Papers'),
        ('maintenance', 'Maintenance'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=255)
    short_description = models.TextField(max_length=500)
    content = RichTextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    @property
    def icon_name(self):
        icons = {
            'news': 'groups',
            'call_for_papers': 'campaign',
            'maintenance': 'build',
            'general': 'info',
        }
        return icons.get(self.category, 'info')

    @property
    def color_class(self):
        colors = {
            'news': 'blue',
            'call_for_papers': 'primary', # Using primary for consistency with design
            'maintenance': 'amber',
            'general': 'gray',
        }
        # This returns the base color name, templates will need to construct the full class
        # e.g. bg-{color}-100 text-{color}-600
        # Wait, primary is a custom color in tailwind config probably, but 'bg-primary/10' is used in template.
        # Let's return a dictionary or object with specific classes to match the design exactly.
        return colors.get(self.category, 'gray')

    @property
    def icon_bg_class(self):
        # Precise mapping to match the template's aesthetics
        if self.category == 'call_for_papers':
            return 'bg-primary/10 text-primary'
        elif self.category == 'news':
            return 'bg-blue-100 dark:bg-blue-900/30 text-blue-600'
        elif self.category == 'maintenance':
            return 'bg-amber-100 dark:bg-amber-900/30 text-amber-600'
        return 'bg-gray-100 dark:bg-gray-800 text-gray-600'

    @property
    def badge_class(self):
        if self.category == 'call_for_papers':
            return 'bg-primary text-white'
        elif self.category == 'news':
            return 'bg-blue-600 text-white'
        elif self.category == 'maintenance':
            return 'bg-amber-600 text-white'
        return 'bg-gray-600 text-white'
