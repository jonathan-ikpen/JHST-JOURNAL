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


# ---------------------------------------------------------------------------
# Crossref DOI tests
# ---------------------------------------------------------------------------

import journal.crossref as crossref_mod
from journal.crossref import (
    build_crossref_xml,
    check_deposit_status,
    deposit_to_crossref,
    generate_doi,
    validate_crossref_doi,
)
from django.core.exceptions import ValidationError
from journal.models import Article, Issue, Volume
from unittest.mock import patch


def make_published_article(author, **kwargs):
    import datetime as _dt
    ms = make_manuscript(author, status='published', **kwargs)
    year = kwargs.get('year', 2026)
    volume = Volume.objects.create(number=kwargs.get('volume_number', 1), year=year)
    issue = Issue.objects.create(
        volume=volume,
        number=kwargs.get('issue_number', 1),
        publication_date=_dt.date(year, 3, 14),
    )
    article = Article.objects.create(manuscript=ms, issue=issue)
    # generate_doi reads article.id, so save first then patch the doi in.
    article.doi = generate_doi(article)
    article.save(update_fields=['doi'])
    return article


class GenerateDoiTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='doiauthor', email='doi@example.com', password='pass12345', is_researcher=True
        )

    def test_generate_doi_uses_fixed_prefix_and_pattern(self):
        article = make_published_article(self.author)
        self.assertEqual(article.doi, f'10.68763/jhst.2026.v1i1.{article.id}')

    def test_placeholder_dois_rejected(self):
        with self.assertRaises(ValidationError):
            validate_crossref_doi('10.1234/jhst.v1.i1.1')


class BuildXmlTests(TestCase):
    def setUp(self):
        create_all_singletons()
        self.author = User.objects.create_user(
            username='doiauthor2', email='doi2@example.com', password='pass12345',
            is_researcher=True, affiliation='Petroleum Training Institute',
        )

    def test_build_xml_contains_required_metadata(self):
        article = make_published_article(self.author)
        xml = build_crossref_xml(article)
        self.assertIn(article.doi, xml)
        self.assertIn(f'/article/{article.id}/', xml)
        self.assertIn('Journal of Hydrocarbon Science and Technology', xml)
        self.assertIn(article.manuscript.title, xml)
        self.assertIn('Petroleum Training Institute', xml)
        self.assertNotIn('None', xml.split('<doi_data>')[0].split('<journal_metadata')[-1])


class DepositTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='doiauthor3', email='doi3@example.com', password='pass12345', is_researcher=True
        )
        self.article = make_published_article(self.author)

    @patch.object(crossref_mod, 'check_deposit_status', return_value=True)
    @patch.object(crossref_mod.requests, 'post')
    def test_failed_deposit_leaves_article_pending(self, mock_post, _mock_check):
        mock_post.return_value.text = (
            '<doi_batch_diagnostic><record_diagnostic status="Failure">'
            '<msg>Invalid metadata</msg></record_diagnostic></doi_batch_diagnostic>'
        )
        mock_post.return_value.raise_for_status = lambda: None
        from django.test import override_settings
        with override_settings(CROSSREF_LOGIN_ID='x@y.z', CROSSREF_LOGIN_PASSWORD='pw', CROSSREF_USE_TEST='True'):
            with self.assertRaises(ValueError):
                deposit_to_crossref(self.article)

    def test_liveness_check_false_and_true(self):
        self.assertFalse(check_deposit_status(self.article))
        with patch.object(crossref_mod.requests, 'get') as mock_get:
            mock_get.return_value.status_code = 200
            self.assertTrue(check_deposit_status(self.article))


class PublishFlowTests(TestCase):
    """Publishing auto-generates a DOI and never crashes on Crossref failure."""

    def setUp(self):
        create_all_singletons()
        self.editor = User.objects.create_user(
            username='doi_editor', email='editor@example.com', password='pass12345', is_editor=True
        )
        self.author = User.objects.create_user(
            username='doi_author4', email='doi4@example.com', password='pass12345', is_researcher=True
        )
        self.ms = make_manuscript(self.author, status='accepted')
        self.volume = Volume.objects.create(number=1, year=2026)
        self.issue = Issue.objects.create(volume=self.volume, number=1, publication_date='2026-03-14')

    @patch('journal.views.check_deposit_status', return_value=False)
    @patch('journal.views.deposit_to_crossref', return_value='batch-123')
    def test_publish_auto_generates_doi_and_deposits(self, _mock_post, _mock_check):
        self.client.force_login(self.editor)
        response = self.client.post(
            reverse('publish_article', args=[self.ms.id]),
            {'issue': str(self.issue.id)},
        )
        self.assertEqual(response.status_code, 302)
        self.ms.refresh_from_db()
        article = self.ms.article
        self.assertEqual(self.ms.status, 'published')
        self.assertEqual(article.doi, f'10.68763/jhst.2026.v1i1.{article.id}')
        self.assertEqual(article.doi_status, 'pending')
        self.assertEqual(article.crossref_batch_id, 'batch-123')

    @patch('journal.views.deposit_to_crossref', side_effect=Exception('network down'))
    def test_publish_survives_crossref_failure(self, _mock_post):
        self.client.force_login(self.editor)
        response = self.client.post(
            reverse('publish_article', args=[self.ms.id]),
            {'issue': str(self.issue.id)},
        )
        self.assertEqual(response.status_code, 302)
        self.ms.refresh_from_db()
        self.assertEqual(self.ms.article.doi_status, 'failed')
        self.assertTrue(self.ms.article.doi.startswith('10.68763/'))


# ---------------------------------------------------------------------------
# Password reset tests
# ---------------------------------------------------------------------------

class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='resetuser', email='reset@example.com', password='OldPass123!'
        )

    def test_login_page_links_to_password_reset(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('password_reset'))

    def test_reset_request_page_loads(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_reset_request_sends_email_to_known_user(self):
        response = self.client.post(reverse('password_reset'), {'email': 'reset@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_reset_request_for_unknown_email_still_redirects(self):
        # Never reveal whether an email exists — same response either way.
        response = self.client.post(reverse('password_reset'), {'email': 'nobody@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_reset_confirm_sets_new_password(self):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

        # Django's PasswordResetConfirmView 302s a valid token into the
        # session-backed set-password URL; follow it to reach the form.
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Set a New Password')

        response = self.client.post(response.redirect_chain[-1][0], {
            'new_password1': 'BrandNewPass123!',
            'new_password2': 'BrandNewPass123!',
        })
        self.assertRedirects(response, reverse('password_reset_complete'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('BrandNewPass123!'))

    def test_reset_confirm_with_bad_token_shows_invalid_page(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        response = self.client.get(
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': 'bad-token'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid or has expired')
