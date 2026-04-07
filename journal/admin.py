from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Manuscript, Review, Volume, Issue, Article, Announcement

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

# Admin Site Customization
admin.site.site_header = "JHST Administration"
admin.site.site_title = "JHST Admin Portal"
admin.site.index_title = "Welcome to Journal of Hydrocarbon Science and Technology Admin Portal"
