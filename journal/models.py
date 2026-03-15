from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sections')
    section_title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(help_text="HTML content for this section")
    image = models.ImageField(upload_to='page_sections/', blank=True, null=True)
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='main')
    order = models.IntegerField(default=0, help_text="Order within chosen location. Leave as 0 to append.")

    def __str__(self):
        return f"{self.get_location_display()}: {self.section_title or f'Section {self.id}'}"

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
