from django.contrib import admin
from .models import (
    HomePage, OrganogramItem, AboutPage, AimScopePage, ContactPage,
    PublicationFeesPage, EditorialTeamPage, TeamMember, IndexingPage,
    IndexingEntry, PoliciesPage, AuthorGuidelinesPage, EthicsMalpracticePage,
    OpenAccessPolicyPage, PeerReviewPolicyPage, ArchivingPolicyPage,
    PlagiarismPolicyPage, SubscriptionAdvertisingPage, EditorialPolicyPage,
    PublicationSchedulePage, GuidelinesPage, ReviewerGuidelinesPage,
    MetricsPage, JhstJournalsPage, PtiJournal, PublicationsPage,
)


class SingletonPageAdmin(admin.ModelAdmin):
    def has_delete_permission(self, _request, _obj=None):
        return False

    def has_add_permission(self, _request):
        return not self.model.objects.exists()


@admin.register(HomePage)
class HomePageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Intro Section', {'fields': ('intro_title', 'video_url')}),
        ('About Section', {'fields': (
            'about_title', 'mission_heading', 'mission_intro',
            'mission_item_1', 'mission_item_2', 'organogram_heading',
        )}),
        ('Chief Editor Section', {'fields': (
            'chief_editor_title', 'chief_editor_photo',
            'chief_editor_para_1', 'chief_editor_para_2',
            'chief_editor_para_3', 'chief_editor_para_4',
            'chief_editor_name', 'chief_editor_role',
        )}),
        ('Sidebar Images', {'fields': ('new_release_image', 'keywords_image')}),
    )


@admin.register(OrganogramItem)
class OrganogramItemAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'color', 'order')
    list_editable = ('order', 'color')
    ordering = ('order',)


@admin.register(AboutPage)
class AboutPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Introduction', {'fields': ('intro_text',)}),
        ('Mission & Vision', {'fields': (
            'mission_heading', 'mission_text',
            'vision_heading', 'vision_text',
        )}),
        ('Objectives', {'fields': (
            'objectives_heading',
            'objective_1', 'objective_2', 'objective_3', 'objective_4',
        )}),
        ('Footer Text', {'fields': ('explore_more_text',)}),
    )


@admin.register(AimScopePage)
class AimScopePageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Intro', {'fields': ('intro_text',)}),
        ('Aim', {'fields': ('aim_heading', 'aim_text')}),
        ('Scope', {'fields': ('scope_heading', 'scope_intro', 'scope_col1', 'scope_col2')}),
    )


@admin.register(ContactPage)
class ContactPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Editorial Office', {'fields': (
            'editorial_office_title',
            'office_journal_name', 'office_department', 'office_institution',
            'office_address_line1', 'office_address_line2',
        )}),
        ('Principal Contact', {'fields': (
            'principal_contact_title',
            'principal_name', 'principal_role', 'principal_email', 'principal_phone',
        )}),
        ('Support Contact', {'fields': (
            'support_contact_title',
            'support_name', 'support_role', 'support_email',
        )}),
    )


@admin.register(PublicationFeesPage)
class PublicationFeesPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Intro', {'fields': ('intro_text',)}),
        ('Article Processing Charge', {'fields': (
            'apc_section_title',
            'international_label', 'international_fee', 'international_currency',
            'domestic_label', 'domestic_fee', 'domestic_currency', 'fee_note',
        )}),
        ('Policies', {'fields': (
            'submission_fees_title', 'submission_fees_text',
            'waiver_policy_title', 'waiver_policy_text',
            'payment_methods_title', 'payment_methods_text',
        )}),
    )


@admin.register(EditorialTeamPage)
class EditorialTeamPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Role Descriptions', {'fields': (
            'editor_in_chief_description', 'managing_director_description', 'editorial_assistant_description',
            'section_editors_description', 'editorial_board_description',
        )}),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_type', 'affiliation', 'email', 'order')
    list_filter = ('role_type',)
    list_editable = ('order',)
    ordering = ('role_type', 'order')


@admin.register(IndexingPage)
class IndexingPageAdmin(SingletonPageAdmin):
    fields = ('intro_text', 'note_text')


@admin.register(IndexingEntry)
class IndexingEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(PoliciesPage)
class PoliciesPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Open Access', {'fields': ('open_access_title', 'open_access_text')}),
        ('Copyright & Licensing', {'fields': ('copyright_title', 'copyright_text')}),
        ('Ethics & Malpractice', {'fields': ('ethics_title', 'ethics_intro_text', 'ethics_items')}),
        ('Peer Review', {'fields': ('peer_review_title', 'peer_review_intro', 'peer_review_steps')}),
        ('Archiving', {'fields': ('archiving_title', 'archiving_text')}),
    )


@admin.register(AuthorGuidelinesPage)
class AuthorGuidelinesPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('About', {'fields': (
            'about_journal_heading', 'about_journal_text',
            'open_access_heading', 'open_access_policy_text',
            'pub_schedule_heading', 'publication_schedule_text',
            'editorial_policy_heading', 'editorial_policy_text',
        )}),
        ('Requirements', {'fields': (
            'general_req_heading', 'general_requirements_text',
            'ms_preparation_heading', 'manuscript_preparation_text',
        )}),
        ('Manuscript Sections', {'fields': (
            'cover_letter_heading', 'cover_letter_text',
            'title_page_heading', 'title_page_text',
            'abstract_heading', 'abstract_text',
            'keywords_heading', 'keywords_text',
            'introduction_heading', 'introduction_text',
            'materials_methods_heading', 'materials_methods_text',
            'result_discussion_heading', 'result_discussion_text',
            'results_heading', 'results_text',
            'discussion_heading', 'discussion_text',
            'conclusion_heading', 'conclusion_text',
            'acknowledgements_heading', 'acknowledgements_text',
            'conflicts_heading', 'conflicts_text',
        )}),
        ('References & Submission', {'fields': (
            'references_heading', 'references_intro_text',
            'submission_heading', 'submission_text',
            'assessment_heading', 'assessment_text',
            'publication_fees_heading', 'publication_fees_text',
            'checklist_heading', 'checklist_items',
        )}),
    )


@admin.register(EthicsMalpracticePage)
class EthicsMalpracticePageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Intro', {'fields': ('intro_text',)}),
        ('Editors', {'fields': ('editors_section_title', 'editors_responsibilities')}),
        ('Reviewers', {'fields': ('reviewers_section_title', 'reviewers_intro_text', 'reviewers_responsibilities')}),
        ('Authors', {'fields': ('authors_section_title', 'authors_responsibilities')}),
        ('Publisher', {'fields': ('publisher_section_title', 'publisher_intro_text', 'publisher_roles')}),
        ('Advisory Board', {'fields': ('advisory_board_title', 'advisory_board_intro_text', 'advisory_board_responsibilities')}),
        ('Human & Animal Rights', {'fields': (
            'human_rights_title', 'human_animal_rights_text',
            'human_participants_subtitle',
            'ethics_approval_heading', 'ethics_approval_text',
            'retrospective_ethics_heading', 'retrospective_ethics_text',
            'retrospective_studies_heading', 'retrospective_studies_text',
            'case_studies_heading', 'case_studies_text',
        )}),
        ('Unethical Behavior Procedures', {'fields': (
            'unethical_behavior_title',
            'identification_heading', 'unethical_behavior_id_items',
            'investigation_heading', 'investigation_items',
            'consequences_heading', 'consequences_items',
            'conflict_interest_heading', 'conflict_of_interest_items',
            'appeals_heading', 'appeals_items',
            'corrections_heading', 'corrections_items',
            'retractions_heading', 'retractions_items',
        )}),
    )


@admin.register(OpenAccessPolicyPage)
class OpenAccessPolicyPageAdmin(SingletonPageAdmin):
    fields = ('intro_text',)


@admin.register(PeerReviewPolicyPage)
class PeerReviewPolicyPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Main Policy', {'fields': ('intro_text', 'process_text', 'desk_rejection_text')}),
        ('Double-Blind Guidelines', {'fields': (
            'guidelines_heading',
            'guidelines_intro', 'guidelines_note',
            'title_page_heading', 'title_page_text',
            'blinded_ms_heading', 'blinded_ms_intro', 'blinded_ms_items',
        )}),
    )


@admin.register(ArchivingPolicyPage)
class ArchivingPolicyPageAdmin(SingletonPageAdmin):
    fields = ('archiving_section_title', 'archiving_text', 'repository_section_title', 'repository_text')


@admin.register(PlagiarismPolicyPage)
class PlagiarismPolicyPageAdmin(SingletonPageAdmin):
    fields = ('intro_text', 'software_text')


@admin.register(SubscriptionAdvertisingPage)
class SubscriptionAdvertisingPageAdmin(SingletonPageAdmin):
    fields = ('intro_text', 'open_access_text')


@admin.register(EditorialPolicyPage)
class EditorialPolicyPageAdmin(SingletonPageAdmin):
    fields = ('intro_text',)


@admin.register(PublicationSchedulePage)
class PublicationSchedulePageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Intro', {'fields': ('intro_text',)}),
        ('Biannual Publication', {'fields': (
            'biannual_title', 'biannual_intro',
            'issue1_month', 'issue1_description',
            'issue2_month', 'issue2_description',
        )}),
        ('Online First', {'fields': ('online_first_title', 'online_first_text')}),
        ('Special Issues', {'fields': ('special_issues_title', 'special_issues_text')}),
    )


@admin.register(GuidelinesPage)
class GuidelinesPageAdmin(SingletonPageAdmin):
    fields = ('intro_text', 'authors_card_description', 'reviewers_card_description')


@admin.register(ReviewerGuidelinesPage)
class ReviewerGuidelinesPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Introduction', {'fields': ('intro_text',)}),
        ('Confidentiality', {'fields': ('confidentiality_title', 'confidentiality_text')}),
        ('Timeliness', {'fields': ('timeliness_title', 'timeliness_text')}),
        ('Scope and Quality', {'fields': ('scope_quality_title', 'scope_quality_text')}),
        ('Review Report', {'fields': (
            'review_report_title', 'review_report_intro',
            'review_report_items', 'review_report_close',
        )}),
        ('Ethical Issues', {'fields': ('ethical_issues_title', 'ethical_issues_text')}),
        ('Benefit to Reviewers', {'fields': ('benefits_title', 'benefits_text')}),
    )


@admin.register(MetricsPage)
class MetricsPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ('Intro', {'fields': ('intro_text',)}),
        ('Key Stats', {'fields': (
            'impact_factor', 'impact_factor_label', 'impact_factor_note',
            'avg_days_first_decision', 'first_decision_label',
            'avg_days_to_publication', 'submission_to_pub_label',
            'acceptance_rate', 'acceptance_rate_label', 'acceptance_rate_note',
        )}),
        ('Usage Statistics', {'fields': (
            'usage_stats_title',
            'full_text_downloads', 'full_text_downloads_label',
            'abstract_views', 'abstract_views_label',
            'unique_visitors', 'unique_visitors_label',
            'countries_reached', 'countries_reached_label',
        )}),
        ('Citation Metrics', {'fields': (
            'citation_metrics_title',
            'total_citations', 'total_citations_label',
            'h_index', 'h_index_label',
            'i10_index', 'i10_index_label',
        )}),
        ('Data Note', {'fields': ('data_updated_note',)}),
    )


@admin.register(JhstJournalsPage)
class JhstJournalsPageAdmin(SingletonPageAdmin):
    fields = ('intro_text',)


@admin.register(PtiJournal)
class PtiJournalAdmin(admin.ModelAdmin):
    list_display = ('name', 'issn', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(PublicationsPage)
class PublicationsPageAdmin(SingletonPageAdmin):
    fields = ('intro_text', 'schedule_frequency_text')
