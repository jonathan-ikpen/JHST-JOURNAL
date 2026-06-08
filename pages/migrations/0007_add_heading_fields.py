from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_aboutpage_intro_text_and_more'),
    ]

    operations = [
        # AboutPage
        migrations.AddField(model_name='aboutpage', name='mission_heading', field=models.CharField(default='Our Mission', max_length=100)),
        migrations.AddField(model_name='aboutpage', name='vision_heading', field=models.CharField(default='Our Vision', max_length=100)),
        migrations.AddField(model_name='aboutpage', name='objectives_heading', field=models.CharField(default='Objectives', max_length=100)),
        migrations.AddField(model_name='aboutpage', name='explore_more_text', field=models.CharField(default='For more specific information, please explore the following sections:', max_length=300)),

        # AimScopePage
        migrations.AddField(model_name='aimscopepage', name='aim_heading', field=models.CharField(default='Aim', max_length=100)),
        migrations.AddField(model_name='aimscopepage', name='scope_heading', field=models.CharField(default='Scope', max_length=100)),

        # ContactPage
        migrations.AddField(model_name='contactpage', name='editorial_office_title', field=models.CharField(default='Editorial Office', max_length=100)),
        migrations.AddField(model_name='contactpage', name='principal_contact_title', field=models.CharField(default='Principal Contact', max_length=100)),
        migrations.AddField(model_name='contactpage', name='support_contact_title', field=models.CharField(default='Support Contact', max_length=100)),

        # PublicationFeesPage
        migrations.AddField(model_name='publicationfeespage', name='apc_section_title', field=models.CharField(default='Article Processing Charge (APC)', max_length=100)),
        migrations.AddField(model_name='publicationfeespage', name='submission_fees_title', field=models.CharField(default='Submission Fees', max_length=100)),
        migrations.AddField(model_name='publicationfeespage', name='waiver_policy_title', field=models.CharField(default='Waiver Policy', max_length=100)),
        migrations.AddField(model_name='publicationfeespage', name='payment_methods_title', field=models.CharField(default='Payment Methods', max_length=100)),

        # PoliciesPage
        migrations.AddField(model_name='policiespage', name='open_access_title', field=models.CharField(default='Open Access Policy', max_length=100)),
        migrations.AddField(model_name='policiespage', name='copyright_title', field=models.CharField(default='Copyright & Licensing', max_length=100)),
        migrations.AddField(model_name='policiespage', name='ethics_title', field=models.CharField(default='Ethics & Malpractice Statement', max_length=100)),
        migrations.AddField(model_name='policiespage', name='peer_review_title', field=models.CharField(default='Peer Review Policy', max_length=100)),
        migrations.AddField(model_name='policiespage', name='archiving_title', field=models.CharField(default='Archiving Policy', max_length=100)),

        # PeerReviewPolicyPage
        migrations.AddField(model_name='peerreviewpolicypage', name='guidelines_heading', field=models.CharField(default='Guidelines for Double-Blind Peer Review', max_length=200)),
        migrations.AddField(model_name='peerreviewpolicypage', name='title_page_heading', field=models.CharField(default='Preparing the Title Page', max_length=200)),
        migrations.AddField(model_name='peerreviewpolicypage', name='blinded_ms_heading', field=models.CharField(default='Preparing the Blinded Manuscript', max_length=200)),

        # ArchivingPolicyPage
        migrations.AddField(model_name='archivingpolicypage', name='archiving_section_title', field=models.CharField(default='Archiving', max_length=100)),
        migrations.AddField(model_name='archivingpolicypage', name='repository_section_title', field=models.CharField(default='Repository', max_length=100)),

        # PublicationSchedulePage
        migrations.AddField(model_name='publicationschedulepage', name='biannual_title', field=models.CharField(default='Biannual Publication', max_length=100)),
        migrations.AddField(model_name='publicationschedulepage', name='online_first_title', field=models.CharField(default='Online First', max_length=100)),
        migrations.AddField(model_name='publicationschedulepage', name='special_issues_title', field=models.CharField(default='Special Issues', max_length=100)),

        # ReviewerGuidelinesPage
        migrations.AddField(model_name='reviewerguidelinespage', name='confidentiality_title', field=models.CharField(default='Confidentiality', max_length=100)),
        migrations.AddField(model_name='reviewerguidelinespage', name='timeliness_title', field=models.CharField(default='Timeliness', max_length=100)),
        migrations.AddField(model_name='reviewerguidelinespage', name='scope_quality_title', field=models.CharField(default='Scope and quality', max_length=100)),
        migrations.AddField(model_name='reviewerguidelinespage', name='review_report_title', field=models.CharField(default='Review report', max_length=100)),
        migrations.AddField(model_name='reviewerguidelinespage', name='ethical_issues_title', field=models.CharField(default='Ethical issues', max_length=100)),
        migrations.AddField(model_name='reviewerguidelinespage', name='benefits_title', field=models.CharField(default='Benefit to reviewers', max_length=100)),

        # MetricsPage
        migrations.AddField(model_name='metricspage', name='impact_factor_label', field=models.CharField(default='Impact Factor', max_length=100)),
        migrations.AddField(model_name='metricspage', name='first_decision_label', field=models.CharField(default='Avg. Time to First Decision', max_length=100)),
        migrations.AddField(model_name='metricspage', name='submission_to_pub_label', field=models.CharField(default='Avg. Submission to Publication', max_length=100)),
        migrations.AddField(model_name='metricspage', name='acceptance_rate_label', field=models.CharField(default='Acceptance Rate', max_length=100)),
        migrations.AddField(model_name='metricspage', name='acceptance_rate_note', field=models.CharField(default='Based on last 12 months', max_length=100)),
        migrations.AddField(model_name='metricspage', name='usage_stats_title', field=models.CharField(default='Usage Statistics', max_length=100)),
        migrations.AddField(model_name='metricspage', name='full_text_downloads_label', field=models.CharField(default='Full Text Downloads', max_length=100)),
        migrations.AddField(model_name='metricspage', name='abstract_views_label', field=models.CharField(default='Abstract Views', max_length=100)),
        migrations.AddField(model_name='metricspage', name='unique_visitors_label', field=models.CharField(default='Unique Visitors', max_length=100)),
        migrations.AddField(model_name='metricspage', name='countries_reached_label', field=models.CharField(default='Countries Reached', max_length=100)),
        migrations.AddField(model_name='metricspage', name='citation_metrics_title', field=models.CharField(default='Citation Metrics', max_length=100)),
        migrations.AddField(model_name='metricspage', name='total_citations_label', field=models.CharField(default='Total Citations', max_length=100)),
        migrations.AddField(model_name='metricspage', name='h_index_label', field=models.CharField(default='h-index (Google Scholar)', max_length=100)),
        migrations.AddField(model_name='metricspage', name='i10_index_label', field=models.CharField(default='i10-index', max_length=100)),

        # EthicsMalpracticePage
        migrations.AddField(model_name='ethicsmalpracticepage', name='editors_section_title', field=models.CharField(default='Responsibilities of Editors and Editorial Board', max_length=200)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='reviewers_section_title', field=models.CharField(default='Responsibilities of Reviewers', max_length=200)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='authors_section_title', field=models.CharField(default='Responsibilities of Authors', max_length=200)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='publisher_section_title', field=models.CharField(default='Roles of the Publisher', max_length=200)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='advisory_board_title', field=models.CharField(default='Responsibilities of the Editorial Advisory Board', max_length=200)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='human_rights_title', field=models.CharField(default='Statement of Human and Animal Rights', max_length=200)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='human_participants_subtitle', field=models.CharField(default='Research involving human participants, their data or biological material', max_length=300)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='ethics_approval_heading', field=models.CharField(default='Ethics approval', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='retrospective_ethics_heading', field=models.CharField(default='Retrospective ethics approval', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='retrospective_studies_heading', field=models.CharField(default='Ethics approval for retrospective studies', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='case_studies_heading', field=models.CharField(default='Ethics approval for case studies', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='unethical_behavior_title', field=models.CharField(default='Procedures for Dealing with Unethical Behavior', max_length=200)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='identification_heading', field=models.CharField(default='Identification', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='investigation_heading', field=models.CharField(default='Investigation', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='consequences_heading', field=models.CharField(default='Consequences', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='conflict_interest_heading', field=models.CharField(default='Conflict of Interest', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='appeals_heading', field=models.CharField(default='Appeals', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='corrections_heading', field=models.CharField(default='Corrections', max_length=100)),
        migrations.AddField(model_name='ethicsmalpracticepage', name='retractions_heading', field=models.CharField(default='Retractions', max_length=100)),

        # AuthorGuidelinesPage
        migrations.AddField(model_name='authorguidelinespage', name='about_journal_heading', field=models.CharField(default='About the Journal', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='open_access_heading', field=models.CharField(default='Open Access Policy', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='pub_schedule_heading', field=models.CharField(default='Publication Schedule', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='editorial_policy_heading', field=models.CharField(default='Editorial Policy', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='general_req_heading', field=models.CharField(default='General Requirements', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='ms_preparation_heading', field=models.CharField(default='Manuscript Preparation', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='cover_letter_heading', field=models.CharField(default='Cover letter', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='title_page_heading', field=models.CharField(default='Title page', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='abstract_heading', field=models.CharField(default='Abstract', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='keywords_heading', field=models.CharField(default='Keywords', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='introduction_heading', field=models.CharField(default='Introduction', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='materials_methods_heading', field=models.CharField(default='Materials and Methods', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='result_discussion_heading', field=models.CharField(default='Result and Discussion', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='results_heading', field=models.CharField(default='Results', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='discussion_heading', field=models.CharField(default='Discussion', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='conclusion_heading', field=models.CharField(default='Conclusion', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='acknowledgements_heading', field=models.CharField(default='Acknowledgements', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='conflicts_heading', field=models.CharField(default='Conflict(s) of Interests', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='references_heading', field=models.CharField(default='References', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='submission_heading', field=models.CharField(default='Submission', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='assessment_heading', field=models.CharField(default='Assessment', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='publication_fees_heading', field=models.CharField(default='Publication Fees', max_length=100)),
        migrations.AddField(model_name='authorguidelinespage', name='checklist_heading', field=models.CharField(default='Submission Preparation Checklist', max_length=100)),
    ]
