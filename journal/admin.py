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

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    fields = ('reviewer', 'due_date', 'comments', 'recommendation')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reviewer":
            kwargs["queryset"] = User.objects.filter(is_reviewer=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ManuscriptAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('title', 'author', 'status', 'submitted_date')
    list_filter = ('status', 'submitted_date')
    search_fields = ('title', 'author__username')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Manuscript, ManuscriptAdmin)
admin.site.register(Review)
admin.site.register(Volume)
admin.site.register(Issue)
admin.site.register(Article)
admin.site.register(Announcement)

# Admin Site Customization
admin.site.site_header = "JHST Administration"
admin.site.site_title = "JHST Admin Portal"
admin.site.index_title = "Welcome to Journal of Hydrocarbon Science and Technology Admin Portal"
