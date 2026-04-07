from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.db import models
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

class PageSectionInline(admin.StackedInline):
    model = PageSection
    extra = 0
    fields = ('section_key', 'content_type', 'order', 'text_content', 'image_content', 'video_url', 'external_link')
    classes = ('collapse',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PageSectionInline]
    list_per_page = 20

# @admin.register(PageSection)
# class PageSectionAdmin(admin.ModelAdmin):
#     list_display = ('page', 'section_key', 'content_type', 'order')
#     search_fields = ('section_key', 'text_content')
#     list_filter = ('page', 'content_type')
#     fields = ('page', 'section_key', 'content_type', 'text_content', 'image_content', 'video_url', 'external_link', 'order')
#     formfield_overrides = {
#         models.TextField: {'widget': CKEditorWidget()},
#     }

# Admin Site Customization
admin.site.site_header = "JHST Administration"
admin.site.site_title = "JHST Admin Portal"
admin.site.index_title = "Welcome to Journal of Hydrocarbon Science and Technology Admin Portal"
