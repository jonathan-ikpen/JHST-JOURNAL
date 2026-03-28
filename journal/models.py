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

# ... (Manuscript, Review, Volume, Issue, Article, Notification, Announcement unchanged) ...

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
        """Returns True if this is a pending round assignment where the author hasn't submitted yet."""
        if self.date_completed:
            return False
        # Check if an author response exists for this specific round yet
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
    content = models.TextField()
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
            'call_for_papers': 'primary', 
            'maintenance': 'amber',
            'general': 'gray',
        }
        return colors.get(self.category, 'gray')

    @property
    def icon_bg_class(self):
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

class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="The URL component for this page (e.g., 'about')")
    template_name = models.CharField(max_length=100, default='journal/page.html', help_text="The template to use for rendering this page")
    meta_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def main_sections(self):
        return self.sections.filter(location='main')

    @property
    def sidebar_sections(self):
        return self.sections.filter(location='sidebar')

    class Meta:
        ordering = ['title']

class PageSection(models.Model):
    LOCATION_CHOICES = [
        ('main', 'Main Content'),
        ('sidebar', 'Sidebar'),
    ]
    SECTION_TYPE_CHOICES = [
        ('STANDARD', 'Standard (Rich Text)'),
        ('VIDEO', 'Vimeo Video'),
        ('ORGANOGRAM', 'Organogram (Leadership List)'),
        ('GRID', '2-Column Grid'),
    ]

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sections')
    section_title = models.CharField(max_length=255, blank=True, null=True)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES, default='STANDARD')
    
    # Standard content
    content = RichTextField(blank=True, null=True, help_text="Text content for standard or grid sections")
    image = models.ImageField(upload_to='page_sections/', blank=True, null=True)
    
    # Video content
    vimeo_url = models.URLField(blank=True, null=True, help_text="Paste the Vimeo video URL here (e.g., https://vimeo.com/12345)")
    
    @property
    def vimeo_id(self):
        if not self.vimeo_url:
            return None
        # Extract ID from various formats like https://vimeo.com/12345 or just 12345
        import re
        match = re.search(r'(\d+)', self.vimeo_url)
        return match.group(1) if match else None

    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='main')
    order = models.IntegerField(default=0, help_text="Order within chosen location. Leave as 0 to append.")

    def __str__(self):
        return f"{self.get_location_display()} ({self.get_section_type_display()}): {self.section_title or f'Section {self.id}'}"

    class Meta:
        ordering = ['location', 'order', 'id']

    def save(self, *args, **kwargs):
        if not self.pk and self.order == 0:
            last_section = PageSection.objects.filter(page=self.page, location=self.location).order_by('-order').first()
            if last_section:
                self.order = last_section.order + 1
            else:
                self.order = 1
        super().save(*args, **kwargs)

class OrganogramItem(models.Model):
    section = models.ForeignKey(PageSection, on_delete=models.CASCADE, related_name='organogram_items')
    number = models.CharField(max_length=10, help_text="e.g., 01, 02")
    title = models.CharField(max_length=255)
    description = models.TextField()
    color_code = models.CharField(max_length=7, default='#00529B', help_text="Hex color code (e.g., #00529B)")
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.number}: {self.title}"

    class Meta:
        ordering = ['order', 'number']
