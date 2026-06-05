import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()

from journal.models import Manuscript, Review, AuthorResponse, User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

def get_or_create_user(username, email, role):
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    if created:
        user.set_password('Password@123')
        if role == 'editor':
            user.is_editor = True
            user.is_staff = True
        elif role == 'reviewer':
            user.is_reviewer = True
        user.save()
    return user

author1 = get_or_create_user("JonathanIkpen", "author1@test.com", "author")
reviewer = get_or_create_user("timothy", "timothy@test.com", "reviewer")
editor = get_or_create_user("jay", "jay@test.com", "editor")

admin_user, _ = User.objects.get_or_create(username="admin", defaults={'email': 'admin@test.com', 'is_superuser': True, 'is_staff': True})
if _: admin_user.set_password('admin')
admin_user.save()

pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Title (Dummy PDF)\n>>\nendobj\ntrailer\n<<\n/Root 1 0 R\n>>\n%%EOF"

def create_dummy_file(name):
    return SimpleUploadedFile(name, pdf_content, content_type="application/pdf")

Manuscript.objects.filter(title__contains="[Screenshot]").delete()

# 1. Manuscript "needs_revision" for Author
m1 = Manuscript.objects.create(
    title="[Screenshot] Hydrological Modeling in Urban Environments",
    abstract="This paper explores the impact of urbanization on local hydrological cycles.",
    author=author1,
    status="needs_revision",
    current_round=1,
    file=create_dummy_file("hydrological_modeling.pdf")
)
Review.objects.create(
    manuscript=m1,
    reviewer=reviewer,
    round=1,
    comments="The methodology needs more detail and clearer charts. Please expand.",
    recommendation="revise",
    is_visible_to_author=True,
    date_completed=timezone.now(),
    invitation_status="accepted"
)

# 2. Manuscript with Pending Review Invitation for Reviewer (timothy)
m2 = Manuscript.objects.create(
    title="[Screenshot] Climate Change Effects on Groundwater",
    abstract="A study on the depletion rates of groundwater under varying climate models.",
    author=author1,
    status="under_review",
    current_round=1,
    file=create_dummy_file("climate_groundwater.pdf")
)
Review.objects.create(
    manuscript=m2,
    reviewer=reviewer,
    round=1,
    invitation_status="invited"
)

# 3. Manuscript where Reviewer accepted but hasn't submitted yet
m3 = Manuscript.objects.create(
    title="[Screenshot] Desalination Efficiency Metrics",
    abstract="Evaluating the energy efficiency of reverse osmosis desalination plants.",
    author=author1,
    status="under_review",
    current_round=1,
    file=create_dummy_file("desalination.pdf")
)
Review.objects.create(
    manuscript=m3,
    reviewer=reviewer,
    round=1,
    invitation_status="accepted"
)

# 4. Manuscript with Completed Reviews for Editor (jay) to Make Decision
m4 = Manuscript.objects.create(
    title="[Screenshot] Sustainable Water Management Practices",
    abstract="Evaluating the long-term sustainability of current water management practices.",
    author=author1,
    status="under_review",
    current_round=1,
    file=create_dummy_file("sustainable_water.pdf")
)
Review.objects.create(
    manuscript=m4,
    reviewer=reviewer,
    round=1,
    comments="Excellent paper, well researched. Recommend accept.",
    recommendation="accept",
    is_visible_to_author=True,
    date_completed=timezone.now(),
    invitation_status="accepted"
)

# 5. Accepted Manuscript ready for publication (Admin)
m5 = Manuscript.objects.create(
    title="[Screenshot] Advanced Techniques in Water Purification",
    abstract="A review of modern nanomaterial-based water purification systems.",
    author=author1,
    status="accepted",
    current_round=1,
    file=create_dummy_file("advanced_purification.pdf")
)

# 6. Manuscript for "Assign Reviewer" (Editor)
m6 = Manuscript.objects.create(
    title="[Screenshot] Assessing River Water Quality Parameters",
    abstract="Analyzing physical and chemical parameters of river water.",
    author=author1,
    status="submitted",
    current_round=1,
    file=create_dummy_file("river_quality.pdf")
)

print("Test data created successfully!")
