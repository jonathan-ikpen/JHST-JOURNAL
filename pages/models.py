from django.db import models
from ckeditor.fields import RichTextField


class SingletonMixin:
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class SiteSettings(SingletonMixin, models.Model):
    issn_online = models.CharField(max_length=50, default='1595 - 431 (Online)')
    issn_print = models.CharField(max_length=50, default='2025(Print)')
    copyright_text = models.CharField(
        max_length=200, 
        default='© 2025 Journal of Hydrocarbon Science & Technology — Petroleum Training Institute, Effurun'
    )

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return "Global Site Settings"


class HomePage(SingletonMixin, models.Model):
    intro_title         = models.CharField(max_length=200, default='An Introduction to the Journal')
    video_url           = models.CharField(max_length=500)
    about_title         = models.CharField(max_length=200)
    mission_heading     = models.CharField(max_length=200)
    mission_intro       = RichTextField()
    mission_item_1      = RichTextField()
    mission_item_2      = RichTextField()
    organogram_heading  = models.CharField(max_length=200)
    chief_editor_title  = models.CharField(max_length=200)
    chief_editor_para_1 = RichTextField()
    chief_editor_para_2 = RichTextField()
    chief_editor_para_3 = RichTextField()
    chief_editor_para_4 = RichTextField()
    chief_editor_name   = models.CharField(max_length=200)
    chief_editor_role   = models.CharField(max_length=200)
    chief_editor_photo  = models.ImageField(upload_to='chief_editor/', blank=True)
    new_release_image   = models.ImageField(upload_to='sidebar/', blank=True)
    keywords_image      = models.ImageField(upload_to='sidebar/', blank=True)

    class Meta:
        verbose_name = 'Home Page'

    def __str__(self):
        return 'Home Page'


class OrganogramItem(models.Model):
    number      = models.CharField(max_length=2)
    title       = models.CharField(max_length=200)
    description = RichTextField()
    color       = models.CharField(max_length=10, help_text='Hex color, e.g. #00529B')
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Organogram Item'

    def __str__(self):
        return f'{self.number} – {self.title}'


class AboutPage(SingletonMixin, models.Model):
    intro_text         = RichTextField()
    mission_heading    = models.CharField(max_length=100, default='Our Mission')
    mission_text       = RichTextField()
    vision_heading     = models.CharField(max_length=100, default='Our Vision')
    vision_text        = RichTextField()
    objectives_heading = models.CharField(max_length=100, default='Objectives')
    objective_1        = RichTextField()
    objective_2        = RichTextField()
    objective_3        = RichTextField()
    objective_4        = RichTextField()
    explore_more_text  = models.CharField(max_length=300, default='For more specific information, please explore the following sections:')

    class Meta:
        verbose_name = 'About Page'

    def __str__(self):
        return 'About Page'


class AimScopePage(SingletonMixin, models.Model):
    intro_text    = RichTextField()
    aim_heading   = models.CharField(max_length=100, default='Aim')
    aim_text      = RichTextField()
    scope_heading = models.CharField(max_length=100, default='Scope')
    scope_intro   = RichTextField()
    scope_col1    = RichTextField(help_text='Enter bullet list content for left column')
    scope_col2    = RichTextField(help_text='Enter bullet list content for right column')

    class Meta:
        verbose_name = 'Aim & Scope Page'

    def __str__(self):
        return 'Aim & Scope Page'


class ContactPage(SingletonMixin, models.Model):
    editorial_office_title = models.CharField(max_length=100, default='Editorial Office')
    office_journal_name    = models.CharField(max_length=200)
    office_department      = models.CharField(max_length=200)
    office_institution     = models.CharField(max_length=200)
    office_address_line1   = models.CharField(max_length=200)
    office_address_line2   = models.CharField(max_length=200)
    principal_contact_title = models.CharField(max_length=100, default='Principal Contact')
    principal_name         = models.CharField(max_length=200)
    principal_role         = models.CharField(max_length=200)
    principal_email        = models.CharField(max_length=200)
    principal_phone        = models.CharField(max_length=50)
    support_contact_title  = models.CharField(max_length=100, default='Support Contact')
    support_name           = models.CharField(max_length=200)
    support_role           = models.CharField(max_length=200)
    support_email          = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Contact Page'

    def __str__(self):
        return 'Contact Page'


class PublicationFeesPage(SingletonMixin, models.Model):
    intro_text             = RichTextField()
    apc_section_title      = models.CharField(max_length=100, default='Article Processing Charge (APC)')
    international_label    = models.CharField(max_length=100)
    international_fee      = models.CharField(max_length=20)
    international_currency = models.CharField(max_length=10)
    domestic_label         = models.CharField(max_length=100)
    domestic_fee           = models.CharField(max_length=20)
    domestic_currency      = models.CharField(max_length=10)
    fee_note               = RichTextField()
    submission_fees_title  = models.CharField(max_length=100, default='Submission Fees')
    submission_fees_text   = RichTextField()
    waiver_policy_title    = models.CharField(max_length=100, default='Waiver Policy')
    waiver_policy_text     = RichTextField()
    payment_methods_title  = models.CharField(max_length=100, default='Payment Methods')
    payment_methods_text   = RichTextField()

    class Meta:
        verbose_name = 'Publication Fees Page'

    def __str__(self):
        return 'Publication Fees Page'


class EditorialTeamPage(SingletonMixin, models.Model):
    editor_in_chief_description     = RichTextField(blank=True)
    managing_director_description   = RichTextField()
    editorial_assistant_description = RichTextField()
    section_editors_description     = RichTextField()
    editorial_board_description     = RichTextField()
    advisory_board_description      = RichTextField(blank=True)

    class Meta:
        verbose_name = 'Editorial Team Page'

    def __str__(self):
        return 'Editorial Team Page'


class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('editor_in_chief',     'Editor-in-Chief'),
        ('managing_director',   'Managing Director'),
        ('editorial_assistant', 'Editorial Assistant'),
        ('section_editor',      'Section Editor'),
        ('editorial_board',     'Editorial Board'),
        ('advisory_board',      'Advisory Board'),
    ]
    name        = models.CharField(max_length=200)
    role_type   = models.CharField(max_length=30, choices=ROLE_CHOICES)
    affiliation = models.CharField(max_length=300)
    photo       = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    bio         = RichTextField()
    email       = models.CharField(max_length=200, blank=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['role_type', 'order']
        verbose_name = 'Team Member'

    def __str__(self):
        return f'{self.name} ({self.get_role_type_display()})'


class IndexingPage(SingletonMixin, models.Model):
    intro_text = RichTextField()
    note_text  = RichTextField()

    class Meta:
        verbose_name = 'Indexing Page'

    def __str__(self):
        return 'Indexing Page'


class IndexingEntry(models.Model):
    name        = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    icon        = models.CharField(max_length=50, help_text='Material icon name, e.g. school')
    url         = models.CharField(max_length=500, blank=True)
    note        = models.CharField(max_length=200, blank=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Indexing Entry'
        verbose_name_plural = 'Indexing Entries'

    def __str__(self):
        return self.name


class PoliciesPage(SingletonMixin, models.Model):
    open_access_title = models.CharField(max_length=100, default='Open Access Policy')
    open_access_text  = RichTextField()
    copyright_title   = models.CharField(max_length=100, default='Copyright & Licensing')
    copyright_text    = RichTextField()
    ethics_title      = models.CharField(max_length=100, default='Ethics & Malpractice Statement')
    ethics_intro_text = RichTextField()
    ethics_items      = RichTextField(help_text='Use CKEditor bullet list for each item')
    peer_review_title = models.CharField(max_length=100, default='Peer Review Policy')
    peer_review_intro = RichTextField()
    peer_review_steps = RichTextField(help_text='Use CKEditor numbered list for each step')
    archiving_title   = models.CharField(max_length=100, default='Archiving Policy')
    archiving_text    = RichTextField()

    class Meta:
        verbose_name = 'Policies Page'

    def __str__(self):
        return 'Policies Page'


class AuthorGuidelinesPage(SingletonMixin, models.Model):
    about_journal_heading       = models.CharField(max_length=100, default='About the Journal')
    about_journal_text          = RichTextField()
    open_access_heading         = models.CharField(max_length=100, default='Open Access Policy')
    open_access_policy_text     = RichTextField()
    pub_schedule_heading        = models.CharField(max_length=100, default='Publication Schedule')
    publication_schedule_text   = RichTextField()
    editorial_policy_heading    = models.CharField(max_length=100, default='Editorial Policy')
    editorial_policy_text       = RichTextField()
    general_req_heading         = models.CharField(max_length=100, default='General Requirements')
    general_requirements_text   = RichTextField()
    ms_preparation_heading      = models.CharField(max_length=100, default='Manuscript Preparation')
    manuscript_preparation_text = RichTextField()
    cover_letter_heading        = models.CharField(max_length=100, default='Cover letter')
    cover_letter_text           = RichTextField()
    title_page_heading          = models.CharField(max_length=100, default='Title page')
    title_page_text             = RichTextField()
    abstract_heading            = models.CharField(max_length=100, default='Abstract')
    abstract_text               = RichTextField()
    keywords_heading            = models.CharField(max_length=100, default='Keywords')
    keywords_text               = RichTextField()
    introduction_heading        = models.CharField(max_length=100, default='Introduction')
    introduction_text           = RichTextField()
    materials_methods_heading   = models.CharField(max_length=100, default='Materials and Methods')
    materials_methods_text      = RichTextField()
    result_discussion_heading   = models.CharField(max_length=100, default='Result and Discussion')
    result_discussion_text      = RichTextField()
    results_heading             = models.CharField(max_length=100, default='Results')
    results_text                = RichTextField()
    discussion_heading          = models.CharField(max_length=100, default='Discussion')
    discussion_text             = RichTextField()
    conclusion_heading          = models.CharField(max_length=100, default='Conclusion')
    conclusion_text             = RichTextField()
    acknowledgements_heading    = models.CharField(max_length=100, default='Acknowledgements')
    acknowledgements_text       = RichTextField()
    conflicts_heading           = models.CharField(max_length=100, default='Conflict(s) of Interests')
    conflicts_text              = RichTextField()
    references_heading          = models.CharField(max_length=100, default='References')
    references_intro_text       = RichTextField()
    submission_heading          = models.CharField(max_length=100, default='Submission')
    submission_text             = RichTextField()
    assessment_heading          = models.CharField(max_length=100, default='Assessment')
    assessment_text             = RichTextField()
    publication_fees_heading    = models.CharField(max_length=100, default='Publication Fees')
    publication_fees_text       = RichTextField()
    checklist_heading           = models.CharField(max_length=100, default='Submission Preparation Checklist')
    checklist_items             = RichTextField(help_text='Use CKEditor bullet list for each checklist item')

    class Meta:
        verbose_name = 'Author Guidelines Page'

    def __str__(self):
        return 'Author Guidelines Page'


class EthicsMalpracticePage(SingletonMixin, models.Model):
    intro_text                       = RichTextField()
    editors_section_title            = models.CharField(max_length=200, default='Responsibilities of Editors and Editorial Board')
    editors_responsibilities         = RichTextField(help_text='Use CKEditor bullet list')
    reviewers_section_title          = models.CharField(max_length=200, default='Responsibilities of Reviewers')
    reviewers_intro_text             = RichTextField()
    reviewers_responsibilities       = RichTextField(help_text='Use CKEditor bullet list')
    authors_section_title            = models.CharField(max_length=200, default='Responsibilities of Authors')
    authors_responsibilities         = RichTextField(help_text='Use CKEditor bullet list')
    publisher_section_title          = models.CharField(max_length=200, default='Roles of the Publisher')
    publisher_intro_text             = RichTextField()
    publisher_roles                  = RichTextField(help_text='Use CKEditor bullet list')
    advisory_board_title             = models.CharField(max_length=200, default='Responsibilities of the Editorial Advisory Board')
    advisory_board_intro_text        = RichTextField()
    advisory_board_responsibilities  = RichTextField(help_text='Use CKEditor bullet list')
    human_rights_title               = models.CharField(max_length=200, default='Statement of Human and Animal Rights')
    human_animal_rights_text         = RichTextField()
    human_participants_subtitle      = models.CharField(max_length=300, default='Research involving human participants, their data or biological material')
    ethics_approval_heading          = models.CharField(max_length=100, default='Ethics approval')
    ethics_approval_text             = RichTextField()
    retrospective_ethics_heading     = models.CharField(max_length=100, default='Retrospective ethics approval')
    retrospective_ethics_text        = RichTextField()
    retrospective_studies_heading    = models.CharField(max_length=100, default='Ethics approval for retrospective studies')
    retrospective_studies_text       = RichTextField()
    case_studies_heading             = models.CharField(max_length=100, default='Ethics approval for case studies')
    case_studies_text                = RichTextField()
    unethical_behavior_title         = models.CharField(max_length=200, default='Procedures for Dealing with Unethical Behavior')
    identification_heading           = models.CharField(max_length=100, default='Identification')
    unethical_behavior_id_items      = RichTextField(help_text='Use CKEditor bullet list')
    investigation_heading            = models.CharField(max_length=100, default='Investigation')
    investigation_items              = RichTextField(help_text='Use CKEditor bullet list')
    consequences_heading             = models.CharField(max_length=100, default='Consequences')
    consequences_items               = RichTextField(help_text='Use CKEditor bullet list')
    conflict_interest_heading        = models.CharField(max_length=100, default='Conflict of Interest')
    conflict_of_interest_items       = RichTextField(help_text='Use CKEditor bullet list')
    appeals_heading                  = models.CharField(max_length=100, default='Appeals')
    appeals_items                    = RichTextField(help_text='Use CKEditor bullet list')
    corrections_heading              = models.CharField(max_length=100, default='Corrections')
    corrections_items                = RichTextField(help_text='Use CKEditor bullet list')
    retractions_heading              = models.CharField(max_length=100, default='Retractions')
    retractions_items                = RichTextField(help_text='Use CKEditor bullet list')

    class Meta:
        verbose_name = 'Ethics & Malpractice Page'

    def __str__(self):
        return 'Ethics & Malpractice Page'


class OpenAccessPolicyPage(SingletonMixin, models.Model):
    intro_text = RichTextField()

    class Meta:
        verbose_name = 'Open Access Policy Page'

    def __str__(self):
        return 'Open Access Policy Page'


class PeerReviewPolicyPage(SingletonMixin, models.Model):
    intro_text           = RichTextField()
    process_text         = RichTextField()
    desk_rejection_text  = RichTextField()
    guidelines_heading   = models.CharField(max_length=200, default='Guidelines for Double-Blind Peer Review')
    guidelines_intro     = RichTextField()
    guidelines_note      = RichTextField()
    title_page_heading   = models.CharField(max_length=200, default='Preparing the Title Page')
    title_page_text      = RichTextField()
    blinded_ms_heading   = models.CharField(max_length=200, default='Preparing the Blinded Manuscript')
    blinded_ms_intro     = RichTextField()
    blinded_ms_items     = RichTextField(help_text='Use CKEditor bullet list for each item')

    class Meta:
        verbose_name = 'Peer Review Policy Page'

    def __str__(self):
        return 'Peer Review Policy Page'


class ArchivingPolicyPage(SingletonMixin, models.Model):
    archiving_section_title  = models.CharField(max_length=100, default='Archiving')
    archiving_text           = RichTextField()
    repository_section_title = models.CharField(max_length=100, default='Repository')
    repository_text          = RichTextField()

    class Meta:
        verbose_name = 'Archiving Policy Page'

    def __str__(self):
        return 'Archiving Policy Page'


class PlagiarismPolicyPage(SingletonMixin, models.Model):
    intro_text   = RichTextField()
    software_text = RichTextField()

    class Meta:
        verbose_name = 'Plagiarism Policy Page'

    def __str__(self):
        return 'Plagiarism Policy Page'


class SubscriptionAdvertisingPage(SingletonMixin, models.Model):
    intro_text      = RichTextField()
    open_access_text = RichTextField()

    class Meta:
        verbose_name = 'Subscription & Advertising Page'

    def __str__(self):
        return 'Subscription & Advertising Page'


class EditorialPolicyPage(SingletonMixin, models.Model):
    intro_text = RichTextField()

    class Meta:
        verbose_name = 'Editorial Policy Page'

    def __str__(self):
        return 'Editorial Policy Page'


class PublicationSchedulePage(SingletonMixin, models.Model):
    intro_text           = RichTextField()
    biannual_title       = models.CharField(max_length=100, default='Biannual Publication')
    biannual_intro       = RichTextField()
    issue1_month         = models.CharField(max_length=50, default='June')
    issue1_description   = models.CharField(max_length=100, default='Issue 1')
    issue2_month         = models.CharField(max_length=50, default='December')
    issue2_description   = models.CharField(max_length=100, default='Issue 2')
    online_first_title   = models.CharField(max_length=100, default='Online First')
    online_first_text    = RichTextField()
    special_issues_title = models.CharField(max_length=100, default='Special Issues')
    special_issues_text  = RichTextField()
    # Publishing Timeline
    timeline_heading      = models.CharField(max_length=100, default='Publishing Timeline', blank=True)
    timeline_stat1_days   = models.CharField(max_length=20, default='7', blank=True)
    timeline_stat1_label  = models.CharField(max_length=200, default='Submission to first decision', blank=True)
    timeline_stat1_tooltip = models.CharField(max_length=300, blank=True, default='')
    timeline_stat2_days   = models.CharField(max_length=20, default='82', blank=True)
    timeline_stat2_label  = models.CharField(max_length=200, default='Submission to decision after review', blank=True)
    timeline_stat2_tooltip = models.CharField(max_length=300, blank=True, default='')
    timeline_stat3_days   = models.CharField(max_length=20, default='201', blank=True)
    timeline_stat3_label  = models.CharField(max_length=200, default='Submission to acceptance', blank=True)
    timeline_stat3_tooltip = models.CharField(max_length=300, blank=True, default='')
    timeline_stat4_days   = models.CharField(max_length=20, default='2', blank=True)
    timeline_stat4_label  = models.CharField(max_length=200, default='Acceptance to online publication', blank=True)
    timeline_stat4_tooltip = models.CharField(max_length=300, blank=True, default='')

    class Meta:
        verbose_name = 'Publication Schedule Page'

    def __str__(self):
        return 'Publication Schedule Page'


class GuidelinesPage(SingletonMixin, models.Model):
    intro_text                 = RichTextField()
    authors_card_description   = RichTextField()
    reviewers_card_description = RichTextField()

    class Meta:
        verbose_name = 'Guidelines Page'

    def __str__(self):
        return 'Guidelines Page'


class ReviewerGuidelinesPage(SingletonMixin, models.Model):
    intro_text               = RichTextField()
    confidentiality_title    = models.CharField(max_length=100, default='Confidentiality')
    confidentiality_text     = RichTextField()
    timeliness_title         = models.CharField(max_length=100, default='Timeliness')
    timeliness_text          = RichTextField()
    scope_quality_title      = models.CharField(max_length=100, default='Scope and quality')
    scope_quality_text       = RichTextField()
    review_report_title      = models.CharField(max_length=100, default='Review report')
    review_report_intro      = RichTextField()
    review_report_items      = RichTextField(help_text='Use CKEditor for term: description list items')
    review_report_close      = RichTextField()
    ethical_issues_title     = models.CharField(max_length=100, default='Ethical issues')
    ethical_issues_text      = RichTextField()
    benefits_title           = models.CharField(max_length=100, default='Benefit to reviewers')
    benefits_text            = RichTextField()

    class Meta:
        verbose_name = 'Reviewer Guidelines Page'

    def __str__(self):
        return 'Reviewer Guidelines Page'


class MetricsPage(SingletonMixin, models.Model):
    intro_text                  = RichTextField()
    impact_factor               = models.CharField(max_length=20)
    impact_factor_label         = models.CharField(max_length=100, default='Impact Factor')
    impact_factor_note          = models.CharField(max_length=50)
    avg_days_first_decision     = models.CharField(max_length=10)
    first_decision_label        = models.CharField(max_length=100, default='Avg. Time to First Decision')
    avg_days_to_publication     = models.CharField(max_length=10)
    submission_to_pub_label     = models.CharField(max_length=100, default='Avg. Submission to Publication')
    acceptance_rate             = models.CharField(max_length=10)
    acceptance_rate_label       = models.CharField(max_length=100, default='Acceptance Rate')
    acceptance_rate_note        = models.CharField(max_length=100, default='Based on last 12 months')
    usage_stats_title           = models.CharField(max_length=100, default='Usage Statistics')
    full_text_downloads         = models.CharField(max_length=20)
    full_text_downloads_label   = models.CharField(max_length=100, default='Full Text Downloads')
    abstract_views              = models.CharField(max_length=20)
    abstract_views_label        = models.CharField(max_length=100, default='Abstract Views')
    unique_visitors             = models.CharField(max_length=20)
    unique_visitors_label       = models.CharField(max_length=100, default='Unique Visitors')
    countries_reached           = models.CharField(max_length=10)
    countries_reached_label     = models.CharField(max_length=100, default='Countries Reached')
    citation_metrics_title      = models.CharField(max_length=100, default='Citation Metrics')
    total_citations             = models.CharField(max_length=20)
    total_citations_label       = models.CharField(max_length=100, default='Total Citations')
    h_index                     = models.CharField(max_length=10)
    h_index_label               = models.CharField(max_length=100, default='h-index (Google Scholar)')
    i10_index                   = models.CharField(max_length=10)
    i10_index_label             = models.CharField(max_length=100, default='i10-index')
    data_updated_note           = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Metrics Page'

    def __str__(self):
        return 'Metrics Page'


class JhstJournalsPage(SingletonMixin, models.Model):
    intro_text = RichTextField()

    class Meta:
        verbose_name = 'JHST Journals Page'

    def __str__(self):
        return 'JHST Journals Page'


class PtiJournal(models.Model):
    name        = models.CharField(max_length=200)
    description = RichTextField()
    issn        = models.CharField(max_length=20)
    url         = models.CharField(max_length=500, blank=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'PTI Journal'

    def __str__(self):
        return self.name


class PublicationsPage(SingletonMixin, models.Model):
    intro_text             = RichTextField()
    schedule_frequency_text = RichTextField()

    class Meta:
        verbose_name = 'Publications Page'

    def __str__(self):
        return 'Publications Page'

class ConferencesPage(SingletonMixin, models.Model):
    intro_text = RichTextField()

    class Meta:
        verbose_name = 'Conferences Page'

    def __str__(self):
        return 'Conferences Page'


class ConferenceProceeding(models.Model):
    title = models.CharField(max_length=200)
    theme = models.CharField(max_length=300)
    date = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='proceedings/covers/')
    pdf_document = models.FileField(upload_to='proceedings/documents/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']
        verbose_name = 'Conference Proceeding'

    def __str__(self):
        return self.title
