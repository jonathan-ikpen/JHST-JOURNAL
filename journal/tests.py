from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from pages.models import (
    HomePage, AboutPage, AimScopePage, ContactPage, PublicationFeesPage,
    EditorialTeamPage, IndexingPage, PoliciesPage, AuthorGuidelinesPage,
    EthicsMalpracticePage, OpenAccessPolicyPage, PeerReviewPolicyPage,
    ArchivingPolicyPage, PlagiarismPolicyPage, SubscriptionAdvertisingPage,
    EditorialPolicyPage, PublicationSchedulePage, GuidelinesPage,
    ReviewerGuidelinesPage, MetricsPage, JhstJournalsPage, PublicationsPage,
)
from .models import Manuscript, Announcement

User = get_user_model()

_SINGLETON_MODELS = [
    HomePage, AboutPage, AimScopePage, ContactPage, PublicationFeesPage,
    EditorialTeamPage, IndexingPage, PoliciesPage, AuthorGuidelinesPage,
    EthicsMalpracticePage, OpenAccessPolicyPage, PeerReviewPolicyPage,
    ArchivingPolicyPage, PlagiarismPolicyPage, SubscriptionAdvertisingPage,
    EditorialPolicyPage, PublicationSchedulePage, GuidelinesPage,
    ReviewerGuidelinesPage, MetricsPage, JhstJournalsPage, PublicationsPage,
]


def create_all_singletons():
    """Ensure every singleton page model has a pk=1 record."""
    for Model in _SINGLETON_MODELS:
        Model.objects.get_or_create(pk=1)


def make_manuscript(author, status='submitted', title=None):
    title = title or f'{status.title()} Paper'
    return Manuscript.objects.create(
        title=title,
        abstract='Test abstract.',
        keywords='keyword1, keyword2',
        file=SimpleUploadedFile(
            f'{status}.pdf', b'%PDF-1.4', content_type='application/pdf'
        ),
        author=author,
        status=status,
    )


# ---------------------------------------------------------------------------
# Public page tests
# ---------------------------------------------------------------------------

class PublicPageTests(TestCase):
    """Every public information page must return HTTP 200."""

    @classmethod
    def setUpTestData(cls):
        create_all_singletons()

    def _ok(self, name, kwargs=None):
        url = reverse(name, kwargs=kwargs) if kwargs else reverse(name)
        resp = self.client.get(url)
        self.assertEqual(
            resp.status_code, 200,
            f"'{name}' returned {resp.status_code} — expected 200",
        )

    # Core / about
    def test_home(self):                      self._ok('index')
    def test_about(self):                     self._ok('about')
    def test_aim_scope(self):                 self._ok('aim_scope')
    def test_contact(self):                   self._ok('contact')
    def test_editorial_team(self):            self._ok('editorial_team')
    def test_publication_fees(self):          self._ok('publication_fees')
    def test_publication_schedule(self):      self._ok('publication_schedule')
    def test_indexing(self):                  self._ok('indexing')
    def test_metrics(self):                   self._ok('metrics')
    def test_jhst_journals(self):             self._ok('jhst_journals')
    def test_publications(self):              self._ok('publications')

    # Guidelines
    def test_guidelines(self):                self._ok('guidelines')
    def test_author_guidelines(self):         self._ok('author_guidelines')
    def test_reviewer_guidelines(self):       self._ok('reviewer_guidelines')

    # Policies
    def test_policies(self):                  self._ok('policies')
    def test_ethics_malpractice(self):        self._ok('ethics_malpractice')
    def test_open_access_policy(self):        self._ok('open_access_policy')
    def test_peer_review_policy(self):        self._ok('peer_review_policy')
    def test_archiving_policy(self):          self._ok('archiving_policy')
    def test_plagiarism_policy(self):         self._ok('plagiarism_policy')
    def test_subscription_advertising(self):  self._ok('subscription_advertising')
    def test_editorial_policy(self):          self._ok('editorial_policy')

    # Announcements & search
    def test_announcements_list(self):        self._ok('announcements')

    def test_search_returns_200(self):
        resp = self.client.get(reverse('search') + '?q=petroleum')
        self.assertEqual(resp.status_code, 200)


# ---------------------------------------------------------------------------
# Auth tests
# ---------------------------------------------------------------------------

class AuthViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_all_singletons()
        cls.password = 'Testpass123!'
        cls.user = User.objects.create_user(
            username='testuser',
            password=cls.password,
            email='test@example.com',
            is_researcher=True,
        )

    def test_login_page_loads(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)

    def test_register_page_loads(self):
        self.assertEqual(self.client.get(reverse('register')).status_code, 200)

    def test_valid_login_authenticates_user(self):
        resp = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': self.password},
            follow=True,
        )
        self.assertTrue(resp.context['user'].is_authenticated)

    def test_wrong_password_is_rejected(self):
        resp = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'wrongpassword'},
        )
        self.assertFalse(resp.wsgi_request.user.is_authenticated)

    def test_logout_ends_session(self):
        self.client.login(username='testuser', password=self.password)
        # Confirm logged in
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)
        # Logout then try dashboard again
        self.client.post(reverse('logout'))
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 302)

    def test_register_creates_user(self):
        count_before = User.objects.count()
        self.client.post(reverse('register'), {
            'username': 'brandnewuser',
            'email': 'brandnew@example.com',
            'password1': 'Complexpass99!',
            'password2': 'Complexpass99!',
        })
        self.assertGreater(User.objects.count(), count_before)


# ---------------------------------------------------------------------------
# Protected-view redirect tests
# ---------------------------------------------------------------------------

class ProtectedViewTests(TestCase):
    """Anonymous users must be redirected to the login page."""

    def _assert_login_required(self, url_name, kwargs=None):
        url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302, f"'{url_name}' should redirect anonymous users")
        self.assertIn('/login/', resp['Location'])

    def test_dashboard_requires_login(self):
        self._assert_login_required('dashboard')

    def test_profile_requires_login(self):
        self._assert_login_required('profile')

    def test_submit_requires_login(self):
        self._assert_login_required('submit_manuscript')

    def test_my_submissions_requires_login(self):
        self._assert_login_required('my_submissions')

    def test_assigned_reviews_requires_login(self):
        self._assert_login_required('assigned_reviews')


# ---------------------------------------------------------------------------
# Dashboard / authenticated-view tests
# ---------------------------------------------------------------------------

class DashboardTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_all_singletons()
        cls.researcher = User.objects.create_user(
            username='researcher', password='Pass123!', is_researcher=True,
        )
        cls.editor = User.objects.create_user(
            username='editor', password='Pass123!', is_editor=True,
        )
        cls.reviewer = User.objects.create_user(
            username='reviewer', password='Pass123!', is_reviewer=True,
        )

    def test_researcher_dashboard_loads(self):
        self.client.login(username='researcher', password='Pass123!')
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)

    def test_editor_dashboard_loads(self):
        self.client.login(username='editor', password='Pass123!')
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)

    def test_submit_page_loads_when_logged_in(self):
        self.client.login(username='researcher', password='Pass123!')
        self.assertEqual(self.client.get(reverse('submit_manuscript')).status_code, 200)

    def test_my_submissions_page_loads(self):
        self.client.login(username='researcher', password='Pass123!')
        self.assertEqual(self.client.get(reverse('my_submissions')).status_code, 200)

    def test_assigned_reviews_page_loads(self):
        self.client.login(username='reviewer', password='Pass123!')
        self.assertEqual(self.client.get(reverse('assigned_reviews')).status_code, 200)

    def test_profile_page_loads(self):
        self.client.login(username='researcher', password='Pass123!')
        self.assertEqual(self.client.get(reverse('profile')).status_code, 200)


# ---------------------------------------------------------------------------
# Manuscript model property tests
# ---------------------------------------------------------------------------

class ManuscriptModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='mauthor', password='pass123')
        cls.submitted    = make_manuscript(cls.author, 'submitted')
        cls.under_review = make_manuscript(cls.author, 'under_review')
        cls.accepted     = make_manuscript(cls.author, 'accepted')
        cls.rejected     = make_manuscript(cls.author, 'rejected')
        cls.published    = make_manuscript(cls.author, 'published')

    # progress_width_class
    def test_submitted_width(self):
        self.assertEqual(self.submitted.progress_width_class, 'w-1/3')

    def test_under_review_width(self):
        self.assertEqual(self.under_review.progress_width_class, 'w-2/3')

    def test_accepted_width(self):
        self.assertEqual(self.accepted.progress_width_class, 'w-full')

    def test_rejected_width(self):
        self.assertEqual(self.rejected.progress_width_class, 'w-full')

    def test_published_width(self):
        self.assertEqual(self.published.progress_width_class, 'w-full')

    # progress_color_class
    def test_rejected_color_is_red(self):
        self.assertEqual(self.rejected.progress_color_class, 'bg-red-500')

    def test_non_rejected_color_is_primary(self):
        for ms in (self.submitted, self.under_review, self.accepted, self.published):
            with self.subTest(status=ms.status):
                self.assertEqual(ms.progress_color_class, 'bg-primary')

    # __str__
    def test_str_returns_title(self):
        self.assertEqual(str(self.submitted), 'Submitted Paper')

    # Manuscript is linked to its author
    def test_author_relationship(self):
        self.assertEqual(self.submitted.author, self.author)


# ---------------------------------------------------------------------------
# Announcement model tests
# ---------------------------------------------------------------------------

class AnnouncementTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_all_singletons()
        cls.ann = Announcement.objects.create(
            title='Test Announcement',
            short_description='Short description.',
            content='<p>Full content here.</p>',
            category='news',
        )

    def test_announcements_list_loads(self):
        self.assertEqual(self.client.get(reverse('announcements')).status_code, 200)

    def test_announcement_detail_loads(self):
        url = reverse('announcement_detail', kwargs={'announcement_id': self.ann.pk})
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_announcement_str(self):
        self.assertEqual(str(self.ann), 'Test Announcement')

    def test_icon_news(self):
        self.assertEqual(self.ann.icon_name, 'groups')

    def test_icon_call_for_papers(self):
        self.assertEqual(Announcement(category='call_for_papers').icon_name, 'campaign')

    def test_icon_maintenance(self):
        self.assertEqual(Announcement(category='maintenance').icon_name, 'build')

    def test_icon_general(self):
        self.assertEqual(Announcement(category='general').icon_name, 'info')

    def test_is_active_default_true(self):
        self.assertTrue(self.ann.is_active)


# ---------------------------------------------------------------------------
# Singleton pattern tests
# ---------------------------------------------------------------------------

class SingletonPatternTests(TestCase):
    """The SingletonMixin must always coerce pk to 1."""

    def test_save_always_sets_pk_to_1(self):
        page = AboutPage()
        page.save()
        self.assertEqual(page.pk, 1)

    def test_multiple_saves_produce_one_record(self):
        AboutPage.objects.all().delete()
        AboutPage().save()
        AboutPage().save()  # Should update, not insert
        self.assertEqual(AboutPage.objects.count(), 1)

    def test_get_or_create_returns_existing_singleton(self):
        AboutPage.objects.all().delete()
        AboutPage().save()
        _, created = AboutPage.objects.get_or_create(pk=1)
        self.assertFalse(created)
        self.assertEqual(AboutPage.objects.count(), 1)


# ---------------------------------------------------------------------------
# User model tests
# ---------------------------------------------------------------------------

class UserModelTests(TestCase):

    def test_create_researcher(self):
        user = User.objects.create_user(
            username='researcher1', password='pass', is_researcher=True,
        )
        self.assertTrue(user.is_researcher)
        self.assertFalse(user.is_editor)
        self.assertFalse(user.is_reviewer)

    def test_create_editor(self):
        user = User.objects.create_user(
            username='editor1', password='pass', is_editor=True,
        )
        self.assertTrue(user.is_editor)

    def test_create_reviewer(self):
        user = User.objects.create_user(
            username='reviewer1', password='pass', is_reviewer=True,
        )
        self.assertTrue(user.is_reviewer)

    def test_user_str_is_username(self):
        user = User(username='johndoe')
        self.assertEqual(str(user), 'johndoe')
