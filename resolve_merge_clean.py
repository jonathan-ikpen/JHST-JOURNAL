import sys
import subprocess

def get_git_file(commit, path):
    return subprocess.check_output(['git', 'show', f'{commit}:{path}']).decode('utf-8')

# Read BOTH files
ours_models = get_git_file('b94ec3d', 'journal/models.py')
theirs_models = get_git_file('origin/dev', 'journal/models.py')

# Extract my CMS code (starts at class Page(models.Model):)
ours_cms = ours_models[ours_models.find('class Page(models.Model):'):]

# Extract their Models up to Notification/Announcement, exactly before their class Page
theirs_main = theirs_models[:theirs_models.find('class Page(models.Model):')]

# Combine them cleanly
final_models = theirs_main + ours_cms

with open('journal/models.py', 'w', encoding='utf-8') as f:
    f.write(final_models)

print("models.py resolved!")

# ----------------- ADMIN.PY -----------------
ours_admin = get_git_file('b94ec3d', 'journal/admin.py')
theirs_admin = get_git_file('origin/dev', 'journal/admin.py')

ours_cms_admin = ours_admin[ours_admin.find('class PageSectionInline'):ours_admin.find('# Admin Site Customization')]
theirs_main_admin = theirs_admin[:theirs_admin.find('class OrganogramItemInline')]

# We must keep their ReviewInline and ManuscriptAdmin, as well as Manuscript registration
theirs_workflow_admin = theirs_admin[theirs_admin.find('class ReviewInline'):theirs_admin.find('admin.site.register(User, CustomUserAdmin)')]

# their admin registers User, Manuscript, etc at the bottom
theirs_registers = theirs_admin[theirs_admin.find('admin.site.register(User, CustomUserAdmin)'):]
theirs_registers = theirs_registers.replace('admin.site.register(Page, PageAdmin)\n', '')
theirs_registers = theirs_registers.replace('admin.site.register(PageSection, PageSectionAdmin)\n', '')

final_admin = theirs_main_admin + "\n" + ours_cms_admin + "\n" + theirs_workflow_admin + "\n" + theirs_registers + """
# Admin Site Customization
admin.site.site_header = "JHST Administration"
admin.site.site_title = "JHST Admin Portal"
admin.site.index_title = "Welcome to Journal of Hydrocarbon Science and Technology Admin Portal"
"""

with open('journal/admin.py', 'w', encoding='utf-8') as f:
    f.write(final_admin)

print("admin.py resolved!")

# ----------------- SETTINGS.PY -----------------
ours_settings = get_git_file('b94ec3d', 'journal_system/settings.py')
theirs_settings = get_git_file('origin/dev', 'journal_system/settings.py')

final_settings = theirs_settings.replace(
    '"journal.context_processors.notifications",',
    '"journal.context_processors.notifications",\n                "journal.context_processors.sidebar_context",'
)

with open('journal_system/settings.py', 'w', encoding='utf-8') as f:
    f.write(final_settings)

print("settings.py resolved!")

# ----------------- VIEWS & URLS -----------------
# For views and urls, our CMS dynamically renders everything via slug. 
ours_views = get_git_file('b94ec3d', 'journal/views.py')
ours_urls = get_git_file('b94ec3d', 'journal/urls.py')
with open('journal/views.py', 'w', encoding='utf-8') as f:
    f.write(ours_views) # Keep our CMS views
with open('journal/urls.py', 'w', encoding='utf-8') as f:
    f.write(ours_urls) # Keep our CMS urls

# Context Processors
with open('journal/context_processors.py', 'w', encoding='utf-8') as f:
    f.write(get_git_file('origin/dev', 'journal/context_processors.py') + "\n" + get_git_file('b94ec3d', 'journal/context_processors.py').replace('from .models import Page\n\n', ''))

print("All unmerged python files resolved!")
