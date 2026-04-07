from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import User, Manuscript, Review, Volume, Issue, Article, Announcement, Page, PageSection

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Affiliation', {'fields': ('is_researcher', 'is_reviewer', 'is_editor', 'affiliation')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Affiliation', {'fields': ('is_researcher', 'is_reviewer', 'is_editor', 'affiliation')}),
    )
    list_display = UserAdmin.list_display + ('is_researcher', 'is_reviewer', 'is_editor', 'affiliation')
    list_filter = UserAdmin.list_filter + ('is_researcher', 'is_reviewer', 'is_editor')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Manuscript)
admin.site.register(Review)
admin.site.register(Volume)
admin.site.register(Issue)
admin.site.register(Article)
admin.site.register(Announcement)

class PageSectionForm(forms.ModelForm):
    class Meta:
        model = PageSection
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We can selectively apply CKEditor widget here if we want, 
        # but since we have a single text_content field, 
        # we'll provide CKEditor by default for better UX, or use formfield_overrides.
        if self.instance and self.instance.content_type == 'html':
             self.fields['text_content'].widget = CKEditorWidget()

class PageSectionInline(admin.TabularInline):
    model = PageSection
    extra = 1
    form = PageSectionForm
    fields = ('section_key', 'content_type', 'text_content', 'image_content', 'order')

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PageSectionInline]
    list_per_page = 20

@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('page', 'section_key', 'content_type', 'order')
    search_fields = ('section_key', 'text_content')
    form = PageSectionForm

# Admin Site Customization
admin.site.site_header = "JHST Administration"
admin.site.site_title = "JHST Admin Portal"
admin.site.index_title = "Welcome to Journal of Hydrocarbon Science and Technology Admin Portal"
