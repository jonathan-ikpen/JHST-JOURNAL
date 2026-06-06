from django.core.management.base import BaseCommand
from pages.models import (
    HomePage, OrganogramItem, AboutPage, AimScopePage, ContactPage,
    PublicationFeesPage, EditorialTeamPage, TeamMember, IndexingPage,
    IndexingEntry, PoliciesPage, AuthorGuidelinesPage, EthicsMalpracticePage,
    OpenAccessPolicyPage, PeerReviewPolicyPage, ArchivingPolicyPage,
    PlagiarismPolicyPage, SubscriptionAdvertisingPage, EditorialPolicyPage,
    PublicationSchedulePage, GuidelinesPage, ReviewerGuidelinesPage,
    MetricsPage, JhstJournalsPage, PtiJournal, PublicationsPage,
)


def _p(*paragraphs):
    """Wrap each argument in a <p> tag."""
    return ''.join(f'<p>{para.strip()}</p>' for para in paragraphs if para and para.strip())


def _ul(text):
    """Convert newline-delimited plain text into <ul><li>…</li></ul> HTML."""
    items = [line.strip() for line in text.split('\n') if line.strip()]
    return '<ul>' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>'


def _ol(text):
    """Convert newline-delimited plain text into <ol><li>…</li></ol> HTML."""
    items = [line.strip() for line in text.split('\n') if line.strip()]
    return '<ol>' + ''.join(f'<li>{item}</li>' for item in items) + '</ol>'


class Command(BaseCommand):
    help = 'Populate all page models with real content from the JHST templates'

    def handle(self, *args, **options):
        self._populate_home_page()
        self._populate_organogram()
        self._populate_about_page()
        self._populate_aim_scope_page()
        self._populate_contact_page()
        self._populate_publication_fees_page()
        self._populate_editorial_team_page()
        self._populate_team_members()
        self._populate_indexing_page()
        self._populate_indexing_entries()
        self._populate_policies_page()
        self._populate_author_guidelines_page()
        self._populate_ethics_malpractice_page()
        self._populate_open_access_policy_page()
        self._populate_peer_review_policy_page()
        self._populate_archiving_policy_page()
        self._populate_plagiarism_policy_page()
        self._populate_subscription_advertising_page()
        self._populate_editorial_policy_page()
        self._populate_publication_schedule_page()
        self._populate_guidelines_page()
        self._populate_reviewer_guidelines_page()
        self._populate_metrics_page()
        self._populate_jhst_journals_page()
        self._populate_pti_journals()
        self._populate_publications_page()

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated all page models with real content.'
        ))

    def _populate_home_page(self):
        # Template wraps mission_intro in <p>, mission_item_* in <li>, and
        # chief_editor_para_* in <p>, so store plain text (no _p() wrapper).
        HomePage.objects.update_or_create(pk=1, defaults={
            'intro_title': 'An Introduction to the Journal',
            'video_url': (
                'https://player.vimeo.com/video/1129153382'
                '?byline=0&title=0&portrait=0&badge=0&autopause=0&player_id=0&app_id=58479'
            ),
            'about_title': 'About the Journal',
            'mission_heading': 'MISSION STATEMENT',
            'mission_intro': (
                'Journal of Hydrocarbon Science and Technology (JHST) is the official '
                'publication of the Petroleum Training Institute, PTI, Effurun, Nigeria. '
                'The journal seeks to:'
            ),
            'mission_item_1': (
                'Provide a global platform for original, peer-reviewed research that deepens '
                'understanding and drives innovation across the hydrocarbon value chain.'
            ),
            'mission_item_2': (
                'Provide the general public with dynamic and required information to the world '
                'for the purpose of innovation, knowledge/education, lifestyle, culture and career development.'
            ),
            'organogram_heading': 'JHST ORGANOGRAM',
            'chief_editor_title': "From the Chief Editor's Desk",
            'chief_editor_para_1': (
                'In an era where the global energy landscape is undergoing unprecedented '
                'transformation, the Journal of Hydrocarbon Science and Technology (JHST) '
                "emerges as a timely response to a critical need. PTI has served as Nigeria's "
                'premier institution for technical excellence in the petroleum and allied sectors. '
                'The JHST is a natural evolution of this legacy.'
            ),
            'chief_editor_para_2': (
                'Our mission at JHST is to provide a global platform for original, peer-reviewed '
                'research that deepens understanding and drives innovation across the hydrocarbon '
                'value chain. We welcome contributions that address both the opportunities and '
                'the challenges of the energy transition.'
            ),
            'chief_editor_para_3': (
                "In line with PTI's commitment to excellence, JHST upholds rigorous standards "
                'of scholarly integrity, transparency, and quality. Our distinguished editorial '
                'and review boards bring together leading experts from around the world.'
            ),
            'chief_editor_para_4': (
                'As we embark on this exciting journey, I invite researchers, industry professionals, '
                'policymakers, and students alike to contribute, collaborate, and engage with JHST. '
                'Welcome to the Journal of Hydrocarbon Science and Technology.'
            ),
            'chief_editor_name': 'Dr. Fredrick B. Owoyemi',
            'chief_editor_role': 'Chief Editor, JHST',
        })
        self.stdout.write('  OK HomePage')

    def _populate_organogram(self):
        # description rendered without |safe in template, store plain text
        items = [
            (1, '01', 'Editor-in-Chief', 'Oversees the whole activities of JHST', '#00529B'),
            (2, '02', 'Managing Editor',
             "Coordinates journal's day-to-day activities, takes correspondences and make "
             'important suggestion on the acceptance or rejection of manuscripts to the editor-in-chief',
             '#B33A3A'),
            (3, '03', 'Editorial Assistant', 'Supports the Managing Editor', '#34A853'),
            (4, '04', 'Section Editor',
             'Checks the appropriateness of a manuscript, handles peer-review and makes '
             'suggestions to the Managing Director',
             '#4A90E2'),
            (5, '05', 'Editorial Board',
             'Make all-inclusive advice to Editor-in-Chief and Managing Editor for better journal indices',
             '#795548'),
        ]
        for order, number, title, description, color in items:
            OrganogramItem.objects.update_or_create(
                order=order,
                defaults={'number': number, 'title': title, 'description': description, 'color': color},
            )
        self.stdout.write('  OK OrganogramItems (5)')

    def _populate_about_page(self):
        AboutPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'Journal of Hydrocarbon Science and Technology (JHST) is the official journal '
                'of the Petroleum Training Institute (PTI), Effurun, Nigeria. It is a premier '
                'open-access, peer-reviewed journal dedicated to disseminating high-quality '
                'research, technical innovations, and policy analyses in the energy sector.'
            ),
            'mission_text': _p(
                'To provide a global platform for the exchange of knowledge between academia '
                'and the hydrocarbon industry, fostering innovation and sustainable development '
                'in energy technologies.'
            ),
            'vision_text': _p(
                'To be a leading authoritative source of scientific and technical information '
                'for the global oil, gas, and energy community.'
            ),
            'objective_1': _p(
                'To publish cutting-edge hypothesis-driven original research, review articles, '
                'and technical notes.'
            ),
            'objective_2': _p(
                'To bridge the gap between theoretical research and practical industrial application.'
            ),
            'objective_3': _p(
                'To inform policy and decision-making in the energy sector through rigorous '
                'scientific analysis.'
            ),
            'objective_4': _p(
                'To support the professional development of scientists, engineers, and '
                'researchers in the hydrocarbon field.'
            ),
        })
        self.stdout.write('  OK AboutPage')

    def _populate_aim_scope_page(self):
        AimScopePage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'The Journal of Hydrocarbon Science and Technology (JHST) is a peer-reviewed, '
                'open-access journal dedicated to the dissemination of high-quality research in '
                'the field of hydrocarbon science, energy technology, and related disciplines.'
            ),
            'aim_text': _p(
                'Our primary aim is to provide a global platform for scientists, engineers, '
                'academicians, and industry professionals to share their innovative research '
                'findings, technical advancements, and reviews. We strive to bridge the gap '
                'between theoretical research and industrial application in the oil and gas sector.'
            ),
            'scope_intro': _p(
                'JHST welcomes original research articles, technical notes, and review papers '
                'in the following areas, though not limited to:'
            ),
            'scope_col1': _ul(
                'Petroleum Geology and Geophysics\n'
                'Reservoir Engineering and Simulation\n'
                'Drilling and Completion Technology\n'
                'Production Engineering and Optimization\n'
                'Natural Gas Engineering and Processing\n'
                'Petrochemicals and Refining Technology'
            ),
            'scope_col2': _ul(
                'Health, Safety, and Environment (HSE) in Energy\n'
                'Energy Economics and Policy\n'
                'Renewable Energy Integration with Hydrocarbons\n'
                'Carbon Capture, Utilization, and Storage (CCUS)\n'
                'Digital Transformation in Oil & Gas (AI, IoT)\n'
                'Pipeline Engineering and Flow Assurance'
            ),
        })
        self.stdout.write('  OK AimScopePage')

    def _populate_contact_page(self):
        ContactPage.objects.update_or_create(pk=1, defaults={
            'office_journal_name': 'Journal of Hydrocarbon Science and Technology',
            'office_department': 'Directorate of Research and Development',
            'office_institution': 'Petroleum Training Institute',
            'office_address_line1': 'P.M.B. 20, Effurun',
            'office_address_line2': 'Delta State, Nigeria.',
            'principal_name': 'Prof. A. B. Johnson',
            'principal_role': 'Editor-in-Chief',
            'principal_email': 'eic@jhst.org',
            'principal_phone': '+234 800 123 4567',
            'support_name': 'Tech Support Team',
            'support_role': 'For technical issues with submission',
            'support_email': 'support@jhst.org',
        })
        self.stdout.write('  OK ContactPage')

    def _populate_publication_fees_page(self):
        PublicationFeesPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'As an Open Access journal, JHST relies on Article Processing Charges (APCs) '
                'to cover the costs of peer review, copyediting, typesetting, long-term '
                'archiving, and journal management.'
            ),
            'international_label': 'International Authors',
            'international_fee': '$20',
            'international_currency': 'USD',
            'domestic_label': 'Domestic Authors (Nigeria)',
            'domestic_fee': '₦30,000',
            'domestic_currency': 'NGN',
            'fee_note': _p(
                '* Fees are subject to change. The applicable fee is the one in effect '
                'at the time of submission.'
            ),
            'submission_fees_text': _p(
                'There are NO submission fees. Authors are only required to pay the APC '
                'after their manuscript has been accepted for publication.'
            ),
            'waiver_policy_text': _p(
                'JHST offers partial or full fee waivers to authors from low-income countries '
                'or those demonstrating genuine financial need. Requests for waivers must be '
                'made at the time of submission.'
            ),
            'payment_methods_text': _p(
                'Payment details (Bank Transfer/Online Payment) will be included in the '
                'acceptance letter. Please do not make any payments until you receive an '
                'official invoice from the Editorial Office.'
            ),
        })
        self.stdout.write('  OK PublicationFeesPage')

    def _populate_editorial_team_page(self):
        EditorialTeamPage.objects.update_or_create(pk=1, defaults={
            'managing_director_description': _p(
                "Oversees the journal's daily editorial operations, manages scholarly "
                'correspondence, and provides informed recommendations to the Editor-in-Chief '
                'regarding manuscript acceptance or rejection.'
            ),
            'editorial_assistant_description': _p(
                'Provides operational and editorial support to the Managing Director in '
                'the administration of journal activities.'
            ),
            'section_editors_description': _p(
                'Assesses the suitability of submitted manuscripts, manages the peer-review '
                'process, and submits informed recommendations to the Managing Director.'
            ),
            'editorial_board_description': _p(
                'Provides comprehensive strategic guidance to the Editor-in-Chief and '
                'Managing Director aimed at enhancing journal quality, visibility, and '
                'indexing performance.'
            ),
        })
        self.stdout.write('  OK EditorialTeamPage')

    def _populate_team_members(self):
        members = [
            {
                'name': 'Professor A. B. Johnson',
                'role_type': 'editor_in_chief',
                'affiliation': 'Department of Petroleum Engineering, Petroleum Training Institute, Effurun, Nigeria',
                'bio': 'Professor Johnson has over 30 years of experience in hydrocarbon research and academia, leading numerous groundbreaking studies in petroleum engineering and sustainable energy transition.',
                'email': 'eic@jhst.org',
                'order': 1,
            },
            {
                'name': 'Dr. C. D. Okafor',
                'role_type': 'managing_director',
                'affiliation': 'Department of Chemical Engineering, PTI Effurun',
                'bio': 'Dr. Okafor specializes in chemical processes and refining technologies, bringing extensive editorial expertise from previous roles in major engineering journals.',
                'email': 'managing.director@jhst.org',
                'order': 1,
            },
            {
                'name': 'Ms. J. K. Bello',
                'role_type': 'editorial_assistant',
                'affiliation': 'Journal of Hydrocarbon Science and Technology',
                'bio': 'Ms. Bello is a dedicated communications professional responsible for managing author relations and streamlining the peer-review timeline.',
                'email': 'admin@jhst.org',
                'order': 1,
            },
            {
                'name': 'Prof. E. F. Mensah',
                'role_type': 'section_editor',
                'affiliation': 'Kwame Nkrumah University of Science and Technology, Ghana',
                'bio': "Prof. Mensah's research focuses on renewable energy integration and biofuels processing technologies.",
                'email': '',
                'order': 1,
            },
            {
                'name': 'Dr. G. H. Smith',
                'role_type': 'section_editor',
                'affiliation': 'University of Aberdeen, United Kingdom',
                'bio': 'Dr. Smith leads research in structural geology and deep-water exploration techniques.',
                'email': '',
                'order': 2,
            },
            {
                'name': 'Prof. I. J. Ahmed',
                'role_type': 'section_editor',
                'affiliation': 'University of Lagos, Nigeria',
                'bio': 'Prof. Ahmed specializes in environmental impact assessments and pollution control in hydrocarbon extraction.',
                'email': '',
                'order': 3,
            },
            {
                'name': 'Dr. K. L. Wong',
                'role_type': 'section_editor',
                'affiliation': 'Universiti Teknologi PETRONAS, Malaysia',
                'bio': 'Dr. Wong brings expertise in digital oilfields, IoT applications, and machine learning models for reservoir prediction.',
                'email': '',
                'order': 4,
            },
            {
                'name': 'Prof. M. N. Opara',
                'role_type': 'editorial_board',
                'affiliation': 'Texas A&M University, USA',
                'bio': 'Recognized globally for contributions to enhanced oil recovery and thermodynamics.',
                'email': '',
                'order': 1,
            },
            {
                'name': 'Prof. P. Q. Roy',
                'role_type': 'editorial_board',
                'affiliation': 'Indian Institute of Technology, India',
                'bio': 'Pioneer in green chemistry applications for hydrocarbon processing.',
                'email': '',
                'order': 2,
            },
            {
                'name': 'Dr. S. T. Utomi',
                'role_type': 'editorial_board',
                'affiliation': 'Shell Research Centre, Netherlands',
                'bio': 'Industry representative bridging the gap between theoretical research and commercial deployment.',
                'email': '',
                'order': 3,
            },
        ]
        for m in members:
            bio_html = _p(m['bio'])
            TeamMember.objects.update_or_create(
                name=m['name'], role_type=m['role_type'],
                defaults={
                    'affiliation': m['affiliation'],
                    'bio': bio_html,
                    'email': m['email'],
                    'order': m['order'],
                },
            )
        self.stdout.write(f'  OK TeamMembers ({len(members)})')

    def _populate_indexing_page(self):
        IndexingPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'The Journal of Hydrocarbon Science and Technology (JHST) is dedicated to '
                'increasing the visibility and impact of published research. We are currently '
                'indexed, abstracted, and listed in the following prestigious databases and directories:'
            ),
            'note_text': _p(
                'We are actively working on including JHST in Scopus and Clarivate Analytics '
                '(Web of Science) to further enhance the global reach of our authors’ work.'
            ),
        })
        self.stdout.write('  OK IndexingPage')

    def _populate_indexing_entries(self):
        entries = [
            (1, 'Google Scholar', 'The world’s largest academic search engine.', 'school', '', ''),
            (2, 'African Journals Online (AJOL)', 'A major platform for African research visibility.', 'public', '', ''),
            (3, 'Crossref', 'Official Digital Object Identifier (DOI) registration agency.', 'link', '', 'Member ID: XXXXX'),
            (4, 'DOAJ', 'Directory of Open Access Journals (Application in Progress).', 'library_books', '', ''),
        ]
        for order, name, description, icon, url, note in entries:
            IndexingEntry.objects.update_or_create(
                order=order,
                defaults={'name': name, 'description': description, 'icon': icon, 'url': url, 'note': note},
            )
        self.stdout.write('  OK IndexingEntries (4)')

    def _populate_policies_page(self):
        PoliciesPage.objects.update_or_create(pk=1, defaults={
            'open_access_text': _p(
                'JHST provides immediate Open Access to its content on the principle that '
                'making research freely available to the public supports a greater global '
                'exchange of knowledge. Users have the right to read, download, copy, '
                'distribute, print, search, or link to the full texts of articles.'
            ),
            'copyright_text': _p(
                'Authors retain the copyright of their work and grant the journal the right '
                'of first publication. Articles are licensed under the Creative Commons '
                'Attribution 4.0 International License (CC BY 4.0), which permits unrestricted '
                'use, distribution, and reproduction in any medium, provided the original author '
                'and source are credited.'
            ),
            'ethics_intro_text': _p(
                'JHST is committed to upholding the highest standards of publication ethics and '
                'takes all possible measures against publication malpractice. We adhere to the '
                'guidelines defined by the Committee on Publication Ethics (COPE).'
            ),
            'ethics_items': _ul(
                'Authorship: Limited to those who have made a significant contribution to the conception, design, execution, or interpretation of the study.\n'
                'Originality and Plagiarism: Authors must ensure their work is entirely original. Plagiarism in any form is unethical and unacceptable.\n'
                'Data Access: Authors should be prepared to provide raw data for editorial review if requested.\n'
                'Conflicts of Interest: All authors must disclose any financial or other substantive conflict of interest.'
            ),
            'peer_review_intro': _p('All submissions to JHST are subject to specific review processes:'),
            'peer_review_steps': _ol(
                'Initial Evaluation: The Editor-in-Chief determines if the manuscript fits the journal’s scope and quality standards.\n'
                'Double-Blind Peer Review: At least two independent reviewers evaluate the manuscript without knowing the authors’ identities (and vice versa).\n'
                'Decision: Based on reviewers’ reports, the Editor makes a decision (Accept, Minor Revision, Major Revision, or Reject).'
            ),
            'archiving_text': _p(
                'JHST utilizes digital archiving systems to ensure the long-term preservation of '
                'its content. Authors are also encouraged to self-archive their accepted manuscripts '
                'in institutional or thematic repositories.'
            ),
        })
        self.stdout.write('  OK PoliciesPage')

    def _populate_author_guidelines_page(self):
        AuthorGuidelinesPage.objects.update_or_create(pk=1, defaults={
            'about_journal_text': _p(
                'The Journal of Hydrocarbon Science and Technology (JHST), the official journal '
                'of the Petroleum Training Institute (PTI), Effurun, Nigeria, is dedicated to '
                'publishing high-quality, peer-reviewed, and hypothesis-driven original research '
                'across all disciplines of hydrocarbon science and technology. JHST provides an '
                'inclusive platform for innovative research from diverse pure and applied sciences fields.',

                'Since its inception, JHST has been recognised for its commitment to academic '
                'excellence. JHST is indexed and abstracted by Scopus, Directory of Open Access '
                'Journals (DOAJ), Google Scholar, and is actively pursuing inclusion in other '
                'major databases.',
            ),
            'open_access_policy_text': _p(
                'This journal ensures immediate open access to its content, embracing the principle '
                'that freely available research fosters a broader global knowledge exchange. Authors '
                'retain full copyright over their work while granting first publication rights to JHST. '
                'All articles in JHST are published under the Creative Commons Attribution 4.0 '
                'International License (CC BY 4.0), allowing for unrestricted use, distribution, and '
                'reproduction, provided proper credit is given to the original authors and source.'
            ),
            'publication_schedule_text': _p(
                'JHST publishes two issues per year and ensures that manuscripts are made available '
                'online as soon as they are accepted.'
            ),
            'editorial_policy_text': _p(
                'Authors must prepare their manuscripts following the Instructions for Authors of '
                'the journal. Manuscripts that do not follow the format and style of the journal '
                'may be returned to the authors for revision or rejected. The Journal reserves the '
                'right to make any further formal changes and language corrections necessary in a '
                'manuscript accepted for publication. Manuscripts are accepted with the understanding '
                'that the authors have not violated the ethics of research and publishing during the '
                'conduct of the experiment and writing of the manuscript.'
            ),
            'general_requirements_text': _p(
                'All submitted manuscripts should contain original research written in the English '
                'Language, not previously published and not under consideration for publication '
                'elsewhere. Manuscripts may be submitted for consideration as original papers '
                '(research articles describing original experimental results) and short '
                'communications. The Journal also publishes mini-reviews, which are by invitation. '
                'However, authors willing to submit a review article may write a proposal for the '
                'editor-in-chief.'
            ),
            'manuscript_preparation_text': _p(
                'The manuscript (including references, tables, boxes, and legends) must be typed '
                'in 12-point font, double-spaced on A4 paper with margins of 1 inch or 4.5 cm on '
                'all sides. All pages in the manuscript should be page-numbered.'
            ),
            'cover_letter_text': _p(
                'The cover letter must clearly show the full contact details with the corresponding '
                "author's postal address(es), phone numbers and e-mail address(es). The relevance "
                'of the study should also be indicated. The cover letter must also disclose all '
                'possible conflicts of interest (e.g. funding sources for consultancies or studies '
                'of products). A minimum of three (3) potential reviewers with their email addresses '
                'and institutions familiar with the subject matter should be suggested. However, the '
                'use of the reviewers is at the discretion of the Editor-in-Chief.'
            ),
            'title_page_text': _p(
                'The title page should contain the title of the manuscript, the authors’ names, '
                'affiliations and email addresses. Additionally, all authors are required to provide '
                'their 16-digit ORCID iD. One of the authors should be designated as the '
                'corresponding author.'
            ),
            'abstract_text': _p(
                'Abstract should not be more than 250 words, containing a concise summary of the '
                'objective and scope, general methods, results, conclusion and significance of the research.'
            ),
            'keywords_text': _p(
                'The journal welcomes a maximum of six keywords, which should be words that can be '
                'used to retrieve the paper, not general words. Words appearing in the title should '
                'not be given as keywords. The keywords must correspond with those in Medical Subject '
                'Headings (MESH) where applicable.'
            ),
            'introduction_text': _p(
                'The Introduction should provide sufficient background on the study. It should also '
                'give the statement of the problem and the rationale for conducting the research. '
                'The aim should also be clearly defined. The contribution to the area of study should '
                'be identified. All these must be presented in logical manner.'
            ),
            'materials_methods_text': _p(
                'This section must provide sufficient detail to allow the work to be reproduced. '
                'Methods already published should be indicated by reference, and only relevant '
                'modifications should be described. Newly developed methods should also be described '
                'in detail. The sources of all major instruments, chemicals, reagents, assay kits '
                'and drugs must be given. The type of statistical tool(s) used to analyse the data '
                'should be mentioned and justified. All procedures involving experimental animals or '
                'human subjects must be accompanied by a statement on ethical approval from an '
                'appropriate ethics committee.'
            ),
            'result_discussion_text': _p('Authors may wish to combine the two sections (Results and Discussion).'),
            'results_text': _p(
                'A clear and concise Results Section should highlight the important results obtained. '
                'Data should be organised into Figures and Tables. The same results should not be '
                'repeated in Figures and Tables. All Tables and Figures should be appropriately '
                'referred to within the text. Values already contained in the Tables need not be '
                'repeated in the Results Section. Qualitative as well as quantitative results should '
                'be included if applicable.'
            ),
            'discussion_text': _p(
                'This section should relate the Results Section to the current understanding of the '
                'scientific problems being investigated in the field. This section, apart from '
                'adducing scientific reason(s) to the results obtained, must also present the '
                'theoretical implications and practical applications of the findings. The authors '
                'should also identify where their findings agree and/or contrast with previously '
                'published studies. Reasons for such differences must also be advanced. This section '
                'must also be devoid of speculations that are not supported by findings in their '
                'present study.'
            ),
            'conclusion_text': _p(
                'The conclusion must reflect the judgment or decision reached by reasoning after '
                'the discussion on the manuscript. This section sums up the arguments about what '
                'you have been writing about.'
            ),
            'acknowledgements_text': _p(
                'Major contributors who did not qualify as authors should be acknowledged '
                'accordingly. Funding sources should also be acknowledged appropriately.'
            ),
            'conflicts_text': _p(
                'Authors are required to disclose financial interests (e.g. employment, significant '
                'share ownership, patent rights, consultancy, research funding, etc.) in any company '
                'or institution that might benefit from their publication. All authors must provide '
                'details of any other potential competing interests of a personal nature that readers '
                'or editors might consider relevant to their publication. To prevent ambiguity, authors '
                'must state explicitly whether potential conflicts exist or do not exist. The statement '
                'should be placed in the text of the submitted manuscript directly following the '
                'Acknowledgements.'
            ),
            'references_intro_text': (
                _p(
                    'All references must be listed at the end of the paper, and authors are responsible '
                    'for ensuring their accuracy. References should be complete and formatted according '
                    'to the Vancouver Reference Format. References are numbered consecutively in order of '
                    'appearance in the text – they are identified by Arabic numerals in parentheses '
                    '(1), square brackets [1], superscript.'
                ) +
                '<div class="space-y-4 text-sm bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">'
                '<p><strong>Books:</strong> Author(s). <em>Title of book</em>. Edition. Place: Publisher; Year.</p>'
                '<p><strong>Journal Articles:</strong> Author(s). Title of article. <em>Abbreviated Journal Title</em>. Year; Volume(Issue): page numbers.</p>'
                '<p><strong>Webpages:</strong> Author(s). Title. [Internet]. Place: Publisher; Date [cited Date]. Available from: URL</p>'
                '<p><strong>Conference Proceedings:</strong> Editor(s). <em>Title of conference</em>. Place: Publisher; Year.</p>'
                '</div>'
            ),
            'submission_text': _p(
                'This should be done ONLY online at the journal website. Submission of the manuscript '
                'through any other means will not be processed.'
            ),
            'assessment_text': _p(
                'Each manuscript will be subjected to both plagiarism check and preliminary editorial '
                'review before it can be sent for double blind peer review. Manuscripts will only be '
                'accepted after satisfactory recommendations have been received from the independent '
                'reviewers. Acceptance of manuscripts for publication will be based on originality '
                'of the research and contribution to scientific knowledge, without neglecting '
                'technical quality.'
            ),
            'publication_fees_text': _p(
                'An article publication fee of Thirty Thousand Naira only (₦30,000.00) or One '
                'Hundred Dollars (100 USD) will be charged on any article accepted for publication. '
                'Payment details will be provided upon acceptance.'
            ),
            'checklist_items': _ul(
                'The manuscript has not been previously published nor under consideration by another journal.\n'
                'The manuscript file is in OpenOffice, Microsoft Word, RTF or WordPerfect document file format.\n'
                'Where available, URLs and DOIs for the references have been provided.\n'
                'The text is double-spaced; uses a 12-point font; employs italics, rather than underlining (except with URL addresses).\n'
                'All illustrations, figures, and tables are placed within the text at the appropriate points rather than at the end.\n'
                'A declaration statement on conflict of interest.\n'
                'A cover letter stating the novelty and significance of the work, and a list of at least three suggested reviewers with their email.'
            ),
        })
        self.stdout.write('  OK AuthorGuidelinesPage')

    def _populate_ethics_malpractice_page(self):
        EthicsMalpracticePage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'The Journal of Hydrocarbon Science and Technology (JHST) is a double-blind '
                'peer-reviewed journal. The Journal Publication Committee is committed to ensuring '
                'that the editorial process of the journal is governed by rigorous ethical and '
                'malpractice standards that are both fair and transparent. We recognize the complex '
                'nature of the scholarly publishing ecosystem which includes the authors, reviewers, '
                'editors, and publishers. As a result, this journal follows the COPE Code of Conduct '
                'and Best Practice Guidelines for Journal Editors and the Code of Conduct for '
                'Journal Publishers.'
            ),
            'editors_responsibilities': _ul(
                'The editors are to determine which manuscripts/articles submitted to the journal should be published. They are to ensure that decisions are made on any submission based on merit only and not on the author’s race, citizenship, religion, ethnicity, gender or political beliefs.\n'
                'The editors are to subject any submitted manuscript to originality test by the use of the appropriate software and send out the blinded copy for the peer-review process.\n'
                'The editors recommend to the Editor-in-Chief, which manuscripts to be accepted or rejected during the review process.\n'
                'Provide the required guidance for the guest editors and the new editorial board members on what is required of them and also keep the existing members up-to-date on new policies and developments.\n'
                'Keeping confidentiality of the authors by ensuring that no information about the author(s) is revealed to the reviewers and vice-versa.\n'
                'Editors are to ensure that no paper is rejected based on suspicion without any valid proof.\n'
                'Editors are to ensure the best international ethical practices by ensuring that all accepted manuscripts meet the international best practices.\n'
                'Ensure that only competent reviewers within a particular field are selected for the review process.\n'
                'The editors shall ensure that materials from all unpublished works submitted to the journal are not used in their work.\n'
                'Ensuring the publication of clarifications, corrections, retractions and apologies when the need arises.\n'
                'The Editor must be responsive and follow the outlined processes in the COPE in a situation where an ethical complaint is made against a submitted or published article.'
            ),
            'reviewers_intro_text': _p(
                'The essence of the peer review process is to assist the editor and the editorial '
                'board in making a publishing decision and also assist the author in improving the '
                'quality of their work by providing critical feedback. With this, the reviewers’ '
                'responsibilities are highlighted:'
            ),
            'reviewers_responsibilities': _ul(
                'Confidentiality: Any information regarding the submitted manuscript should be strictly kept confidential and shouldn’t be discussed with a third party without the permission of the editor.\n'
                'Conflict of interest: If any of the reviewers have a conflict of interest in any manuscript resulting from a collaboration, competition, or any other connection with any of the authors, companies, or institutions connected to the papers, the reviewer should not consider the manuscript.\n'
                'Unbiasedness: The reviewers should consider the manuscript objectively without any consideration of the authors’ race, religion, ethnicity, political affiliation, age, or whatsoever.\n'
                'Objectivity: The assessment by the reviewers should be conducted objectively, supported with data and the arguments should be clearly expressed without personal criticism of any of the authors.\n'
                'Celerity: The review should be conducted promptly as stipulated by the editor and if a potential reviewer feels unqualified to assess the manuscript, he/she should withdraw from the review process and notify the editor immediately for a timely replacement.\n'
                'Acknowledgement of sources and relevant works: The reviewers must make sure that the authors have acknowledged and cited all sources of data used in the research. Any copyrighted pictures should be used with permission and any relevant published work that has not been cited by the authors should be identified.\n'
                'Plagiarism and other ethical concerns: The reviewers should notify the editor if they suspect any plagiarism or other unethical practices concerning the manuscript.'
            ),
            'authors_responsibilities': _ul(
                'Authorship of the Paper: Authorship should be limited to all those who have made substantial contributions to the conception, design, execution and analysis/interpretation of data including draft preparation. All authors are to take collective responsibility for the reported work.\n'
                'Originality: Authors must ensure that the submitted article is original in content and has not been previously published or is being considered for publication elsewhere.\n'
                'Human and animal welfare: It is the duty of the authors to ensure that adequate consideration has been given to the welfare of human and animal subjects used in the work.\n'
                'Declaration of any conflict of interest: Authors must declare any conflict of interest that may arise from an article. This should include the source of funding for the work.\n'
                'Avoidance of plagiarism: Authors must ensure that the works of others are properly cited and efforts should be made to avoid word-for-word copies of other people’s works.'
            ),
            'publisher_intro_text': _p('The roles of the JHST Committee in scientific communication include:'),
            'publisher_roles': _ul(
                'To provide practical support to the Editor-in-Chief and Editorial Board in following the COPE Code of Conduct for journals.\n'
                'To ensure the autonomy of editorial decisions.\n'
                'To protect intellectual property and copyright, and arbitrate in disputes (e.g., over ethics, authorship).\n'
                'To carry out copy-editing, proofreading, type-setting and styling of materials.\n'
                'To ensure the linking of articles to open and accessible databases.\n'
                'To arrange and manage scholarly peer review.\n'
                'To maintain the scholarly record.\n'
                'To disseminate research data to researchers and other stakeholders such as policymakers, economic, biomedical and industrial practitioners as well as the general public.\n'
                'To manage the processes of quality assurance, interlinking and findability of research.\n'
                'To ensure transparency about the nature and the quality of the services offered as a publisher.'
            ),
            'advisory_board_intro_text': _p(
                'Maintaining JHST as a scientific journal of the highest quality depends a lot on '
                'the Editorial Advisory Board. As a member of the Editorial Advisory Board of JHST, '
                'you are expected to add value and academic credibility to JHST in the following ways:'
            ),
            'advisory_board_responsibilities': _ul(
                'Work with the Editor-in-Chief and advise him on issues that should be addressed by the journal as well as the overall scope and focus of the journal.\n'
                'Promote the journal whenever and wherever possible by sourcing new submissions and making the most of their academic/industry contacts in the journal’s subject areas.\n'
                'May be requested to review papers and undertake book reviews.\n'
                'May be required to contribute to the journal content by contributing submissions as Guest Editors.'
            ),
            'human_animal_rights_text': _p(
                'When reporting experiments on human subjects, authors should indicate whether the '
                'procedures followed were in accordance with the ethical standards of the responsible '
                'committee on human experimentation (institutional and national) and with the Helsinki '
                'Declaration of 1975, as revised in 2000.',

                'Authors of manuscripts that describe experimental studies on either humans or animals '
                'must supply a statement that the study was approved by an institutional review '
                'committee or ethics committee and that the subjects gave informed consent.'
            ),
            'ethics_approval_text': _p(
                'When reporting a study that involved human participants, their data or biological '
                'material, authors should include a statement that confirms that the study was approved '
                '(or granted exemption) by the appropriate institutional and/or national research ethics '
                'committee (including the name of the ethics committee) and certify that the study was '
                'performed in accordance with the ethical standards as laid down in the 1964 Declaration '
                'of Helsinki and its later amendments or comparable ethical standards.'
            ),
            'retrospective_ethics_text': _p(
                'If a study has not been granted ethics committee approval prior to commencing, '
                'retrospective ethics approval usually cannot be obtained and it may not be possible '
                'to consider the manuscript for peer review. The decision on whether to proceed to '
                'peer review in such cases is at the Editor’s discretion.'
            ),
            'retrospective_studies_text': _p(
                'Although retrospective studies are conducted on already available data or biological '
                'material (for which formal consent may not be needed or is difficult to obtain) ethics '
                'approval may be required depending on the law and the national ethical guidelines of a country.'
            ),
            'case_studies_text': _p(
                'Case reports require ethics approval. Most institutions will have specific policies '
                'on this subject. Authors should check with their institution to make sure they are '
                'complying with the specific requirements of their institution and seek ethics approval '
                'where needed.'
            ),
            'unethical_behavior_id_items': _ul(
                'Unethical behaviour can be identified and reported to journal editors and/or the publisher at any time.\n'
                'Unethical practices may include but are not limited to, violations of any of the above-mentioned Ethical Expectations (e.g., plagiarism, falsification or fabrication, authorship falsification, redundant publication, undeclared conflict of interest, etc.).\n'
                'For an investigation to be conducted, the person reporting the ethical breach must provide sufficient evidence. Until a conclusion is reached, all allegations are treated equally and seriously.'
            ),
            'investigation_items': _ul(
                'The journal’s editor will investigate not usually alone but in consultation with JHST.\n'
                'To avoid defamation, evidence gathering will be done so that allegations are only shared with those who need to know.\n'
                'The investigation will be completed within a reasonable time after the allegation is made.\n'
                'The accused party will be notified and allowed to respond to the allegation as part of the investigation.\n'
                'If the allegation(s) are valid as part of the investigation, the severity of the breach will be determined.\n'
                'Cases beyond the editor’s investigative capabilities (e.g., data fabrication or theft) will be referred to the author’s institution with a request for an investigation.'
            ),
            'consequences_items': _ul(
                'Informing the author or reviewer of the misconduct breach in cases where there appears to be a misunderstanding of ethical standards.\n'
                'Sending a strongly worded letter to the author or reviewer outlining the breach and warning against future behaviour.\n'
                'Publishing an erratum notice outlining the ethical breach.\n'
                'Sending a formal letter to the author’s or reviewer’s employer or funding agency.\n'
                'Undertaking a formal retraction or withdrawal of the work in question from the journal, as well as informing indexing services and readers of the misconduct.\n'
                'Imposing a formal embargo on submissions from an individual for a fixed period.\n'
                'Reporting the misconduct to a regulatory association for review and action.'
            ),
            'conflict_of_interest_items': _ul(
                'All authors must disclose any commercial associations or other arrangements (e.g., financial compensation received, patient-licensing arrangements, the potential for profit, consultancy, stock ownership, etc.) that may pose a conflict of interest in connection with the article.\n'
                'Editors and reviewers must recuse themselves from evaluating papers in which they may have a conflict of interest.'
            ),
            'appeals_items': _ul(
                'Authors have the right to appeal decisions. All appeals will be reviewed on a case-by-case basis by journal editors. The journal editors will recuse themselves depending on the nature of the appeal, and the appeal will be reviewed by a different member of the journal’s editorial team.'
            ),
            'corrections_items': _ul(
                'Authors must notify the journal’s editor of any factual errors they discover or are informed of in a published article. When corrections are required, they are made quickly and are accompanied by an errata notice that describes the correction.'
            ),
            'retractions_items': _ul(
                'The editors consider retractions when there is evidence of untrustworthy data or findings, plagiarism, duplicate publication, or unethical research. If an article is under investigation, we may consider an expression of concern notice.\n'
                'In exceptional circumstances, the original article may be removed for legal reasons. In such cases, the metadata will be kept, while the original text will be replaced with the retraction note and a note explaining why the article was removed for legal reasons.'
            ),
        })
        self.stdout.write('  OK EthicsMalpracticePage')

    def _populate_open_access_policy_page(self):
        OpenAccessPolicyPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'This journal provides immediate open access to its content on the principle that '
                'making research freely available to the public supports a greater global exchange '
                'of knowledge. Authors retain copyright of their work, with first publication rights '
                'granted to Journal of Hydrocarbon Science and Technology (JHST). Articles in JHST '
                'are published on the Creative Commons Attribution 4.0 International license (CC BY 4.0).'
            ),
        })
        self.stdout.write('  OK OpenAccessPolicyPage')

    def _populate_peer_review_policy_page(self):
        PeerReviewPolicyPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'The Journal of Hydrocarbon Science and Technology (JHST) operates a Double-Blind '
                'Peer Review Policy. The double-blind peer review procedure guarantees objectivity '
                'and avoids prejudice during the review process. When a review is conducted '
                'double-blindly, neither the reviewer nor the author knows each other’s identity. '
                'This improves neutrality and prevents potential biases from skewing the reviewer’s '
                'judgment. Double-blind peer review not only increases the process’s efficacy as '
                'an academic journal quality control method but also makes it more equitable for all '
                'parties involved.'
            ),
            'process_text': _p(
                'The JHST double-blind review process begins with submitting your manuscript; our '
                'editor decides whether your paper is a good fit based on our pre-review assessment, '
                'which includes a plagiarism check and conformity with the authors’ guidelines. '
                'If the editor is satisfied with the pre-assessment of the manuscript, a copy without '
                'the author’s details is sent to at least two reviewers by the editor. Reviewers '
                'may see the paper’s title and introduction, but they do not know who wrote it. '
                'The reviewer will then review your paper and send comments and recommendations to '
                'the editor, and the editor will then return the paper to you with their comments. '
                'These steps are repeated until both reviewers agree that the paper is ready for publication.'
            ),
            'desk_rejection_text': _p(
                'At JHST, a desk rejection is usually decided within the first week after submission '
                'if the article is not aligned with the journal’s interests or objectives or if '
                'a very preliminary version has been submitted (with errors, shortcomings, or a poorly '
                'developed argument). The double-blind peer review process is followed for all articles '
                'published in JHST.'
            ),
            'guidelines_intro': _p(
                'JHST employs double-blind peer review for all its articles; as a result, both the '
                'author and reviewer are anonymous to one another. To ensure the success of this '
                'process, the author(s) need to ensure that their manuscripts are prepared in a manner '
                'that does not reveal their identity.'
            ),
            'guidelines_note': _p(
                'To help the author(s) prepare their manuscript, authors should be guided by the '
                'outlined points when submitting to the Journal of Hydrocarbon Science and Technology.'
            ),
            'title_page_text': _p(
                'The title page should contain the title, authors’ names and affiliations, and a '
                'complete address for the corresponding author, including telephone and e-mail addresses.'
            ),
            'blinded_ms_intro': _p(
                'To guarantee that the article is appropriately ready for double-blind peer review, '
                'additional actions must be taken in addition to the evident necessity of removing '
                'names and affiliations from the paper’s title. The following are the essential '
                'things to keep an eye on to facilitate this process:'
            ),
            'blinded_ms_items': _ul(
                'When referencing the Authors’ prior work, use the third person case. For example, instead of saying “as we have shown in our previous work,” say “has shown by (Anonymous, 2023)”.\n'
                'Ensure that tables or figures do not contain any pointer to the author’s affiliation.\n'
                'Eliminate all mentions of financing sources.\n'
                'Leave out the acknowledgements.\n'
                'Make sure document properties are anonymized and remove any identifiable information from file names, such as author names.\n'
                'Refrain from removing necessary self-references or other references, and restrict self-references to sources that will interest the reviewer of the submitted work.'
            ),
        })
        self.stdout.write('  OK PeerReviewPolicyPage')

    def _populate_archiving_policy_page(self):
        ArchivingPolicyPage.objects.update_or_create(pk=1, defaults={
            'archiving_text': _p(
                'Journal of Hydrocarbon Science and Technology is archived in the Open Journal System '
                '(OJS) Public Knowledge Project Preservation Network (PKP PN).'
            ),
            'repository_text': _p(
                'Journal of Hydrocarbon Science and Technology permits the authors to self-archive All '
                'Versions of their work (this includes, the original version (Submitted manuscript), '
                'Accepted Version (Author accepted manuscript) and the published Version (Version of '
                'record)) in their personal website or in an institutional repository and any other '
                'repositories of their choice for as long as the author wishes. However, the published '
                'source must be acknowledged. For articles, a link to the journal homepage or Digital '
                'Object Identifier (DOI) of the article must be set.'
            ),
        })
        self.stdout.write('  OK ArchivingPolicyPage')

    def _populate_plagiarism_policy_page(self):
        PlagiarismPolicyPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'Each manuscript will be subjected to a plagiarism check before being sent for '
                'double-blind peer review. Manuscripts will only be processed for peer review if '
                'the similarity index is not more than ten (10) percent.'
            ),
            'software_text': _p(
                'This Journal uses Plagiarism CheckerX (or equivalent industry standard software) '
                'for its similarity index check.'
            ),
        })
        self.stdout.write('  OK PlagiarismPolicyPage')

    def _populate_subscription_advertising_page(self):
        SubscriptionAdvertisingPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'For details on our subscription and advertising policies, kindly visit our '
                'Contact page or email the managing editor.'
            ),
            'open_access_text': _p(
                'As an Open Access journal, subscription fees do not apply for reading the content.'
            ),
        })
        self.stdout.write('  OK SubscriptionAdvertisingPage')

    def _populate_editorial_policy_page(self):
        EditorialPolicyPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'Authors must prepare their manuscripts in accordance with the Instructions for '
                'Authors of the journal. Manuscripts which do not follow the format and style of '
                'the Journal may be returned to the authors for revision or rejected. The Journal '
                'reserves the right to make any further formal changes and language corrections '
                'necessary in a manuscript accepted for publication. Manuscripts are accepted with '
                'the understanding that the authors have not violated the ethics of research and '
                'publishing during the conduct of the experiment and writing of the manuscript.'
            ),
        })
        self.stdout.write('  OK EditorialPolicyPage')

    def _populate_publication_schedule_page(self):
        PublicationSchedulePage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'The Journal of Hydrocarbon Science and Technology (JHST) adheres to a regular '
                'publication schedule to ensure timely dissemination of research.'
            ),
            'biannual_intro': _p('JHST publishes two regular issues per calendar year:'),
            'online_first_text': _p(
                'To minimize publication lag, accepted articles are published individually online '
                'as “Articles in Press” immediately after final proofreading, before they '
                'are assigned to a specific issue. This ensures your research is available to the '
                'community as quickly as possible.'
            ),
            'special_issues_text': _p(
                'The journal occasionally publishes Special Issues focused on emerging topics or '
                'conference proceedings. Calls for papers for special issues are announced in the '
                'Announcements section.'
            ),
            'timeline_heading': 'Publishing Timeline',
            'timeline_stat1_days': '7',
            'timeline_stat1_label': 'Submission to first decision',
            'timeline_stat1_tooltip': 'Median number of days from submission receipt to first editorial decision',
            'timeline_stat2_days': '82',
            'timeline_stat2_label': 'Submission to decision after review',
            'timeline_stat2_tooltip': 'Median number of days from submission to decision following peer review',
            'timeline_stat3_days': '201',
            'timeline_stat3_label': 'Submission to acceptance',
            'timeline_stat3_tooltip': 'Median number of days from submission to final acceptance',
            'timeline_stat4_days': '2',
            'timeline_stat4_label': 'Acceptance to online publication',
            'timeline_stat4_tooltip': 'Median number of days from acceptance to online publication',
        })
        self.stdout.write('  OK PublicationSchedulePage')

    def _populate_guidelines_page(self):
        GuidelinesPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p('Please select the appropriate guidelines from the sections below:'),
            'authors_card_description': _p(
                'Comprehensive instructions for manuscript preparation, formatting, submission '
                'requirements, and information on publication fees.'
            ),
            'reviewers_card_description': _p(
                'Information for peer reviewers regarding confidentiality, evaluation criteria, '
                'report structure, and benefits.'
            ),
        })
        self.stdout.write('  OK GuidelinesPage')

    def _populate_reviewer_guidelines_page(self):
        ReviewerGuidelinesPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'Thank you for agreeing to review a manuscript for JHST. Your review will help us '
                'maintain our journal’s high quality and relevance. Please read the following '
                'instructions carefully before you start your review.'
            ),
            'confidentiality_text': _p(
                'The manuscript you are reviewing should not be shared or discussed with anyone '
                'outside the review process. You should also not use any information or data from '
                'the manuscript for your benefit or advantage. If you have any conflicts of interest '
                'with the manuscript or the authors, please inform the editorial office immediately '
                'and decline the review invitation.'
            ),
            'timeliness_text': _p(
                'Please complete your review within four weeks from the invitation date. If you need '
                'more time or cannot complete the review, please get in touch with the editorial '
                'office as soon as possible and suggest alternative reviewers if possible.'
            ),
            'scope_quality_text': _p(
                'Please evaluate the manuscript according to its scope, originality, significance, '
                'quality, and clarity. The manuscript should fit the aims and scope of JHST and '
                'contribute substantially to the fields of Hydrocarbon Science and Technology. The '
                'manuscript should also be well-written, well-structured, well-referenced, and free '
                'of errors and plagiarism.'
            ),
            'review_report_intro': _p(
                'Please provide a detailed and constructive review report to help the authors improve '
                'their manuscript and the editor decide. Your report should include the following sections:'
            ),
            'review_report_items': _ul(
                'Summary: Provide a summary of the manuscript’s main aim, findings, and strengths.\n'
                'General comments: Provide your overall assessment of the manuscript, highlighting its merits and weaknesses and suggesting major revisions or improvements if needed.\n'
                'Specific comments: Provide specific comments on each section of the manuscript, pointing out any errors, inconsistencies, ambiguities, or suggestions for improvement.\n'
                'Recommendation: Provide your recommendation for the next processing stage of the manuscript.'
            ),
            'review_report_close': _p('Please justify your recommendation with clear and objective arguments.'),
            'ethical_issues_text': _p(
                'Please report any ethical issues or concerns that you may have about the manuscript, '
                'such as plagiarism, fabrication, falsification, duplication, unethical research '
                'practices, or conflicts of interest.'
            ),
            'benefits_text': _p(
                'Reviewers who have reviewed for the journal shall have the benefit of a twenty per '
                'cent (20%) waiver when publishing with the journal in our subsequent two editions, '
                'and this does not preclude a letter of appreciation to the reviewers after the '
                'completion of their review.'
            ),
        })
        self.stdout.write('  OK ReviewerGuidelinesPage')

    def _populate_metrics_page(self):
        MetricsPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'These metrics provide a snapshot of the journal’s performance, impact, and reach. '
                'JHST values transparency and aims to provide authors and readers with up-to-date statistics.'
            ),
            'impact_factor': '2.45',
            'impact_factor_note': 'Estimated',
            'avg_days_first_decision': '45',
            'avg_days_to_publication': '68',
            'acceptance_rate': '32%',
            'full_text_downloads': '15,420',
            'abstract_views': '48,901',
            'unique_visitors': '22,050',
            'countries_reached': '85',
            'total_citations': '342',
            'h_index': '12',
            'i10_index': '15',
            'data_updated_note': 'Data Last Updated: January 1, 2025. Source: Internal Journal Analytics & Google Scholar.',
        })
        self.stdout.write('  OK MetricsPage')

    def _populate_jhst_journals_page(self):
        JhstJournalsPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p(
                'The Petroleum Training Institute (PTI) publishes a range of academic journals '
                'covering various technical, vocational, and scientific disciplines. Explore our '
                'other journals below:'
            ),
        })
        self.stdout.write('  OK JhstJournalsPage')

    def _populate_pti_journals(self):
        journals = [
            (1, 'Journal of Mechanical Engineering Technology (JMET)',
             'Focuses on advances in mechanical systems, manufacturing processes, robotics, and industrial engineering applications.',
             '1234-5678', '#'),
            (2, 'PTI Electrical Engineering Review (PEER)',
             'Dedicated to research in electrical power systems, control engineering, electronics, and telecommunications technology.',
             '2345-6789', '#'),
            (3, 'Journal of Industrial Safety and Environmental Technology (JISET)',
             'A multidisciplinary journal covering occupational safety, environmental impact assessment, and waste management.',
             '8765-4321', '#'),
            (4, 'Petroleum Business Review (PBR)',
             'Focusing on the economics, policy, management, and legal aspects of the petroleum and energy industry.',
             '9988-7766', '#'),
        ]
        for order, name, description, issn, url in journals:
            PtiJournal.objects.update_or_create(
                order=order,
                defaults={'name': name, 'description': _p(description), 'issn': issn, 'url': url},
            )
        self.stdout.write('  OK PtiJournals (4)')

    def _populate_publications_page(self):
        PublicationsPage.objects.update_or_create(pk=1, defaults={
            'intro_text': _p('Browse our database of published issues and articles. JHST publishes biannually, with occasional special issues.'),
            'schedule_frequency_text': _p(
                'Frequency: Two issues per year (June and December).',
                'Articles are published online immediately upon acceptance and final processing (Online First), before being assigned to an issue.',
            ),
        })
        self.stdout.write('  OK PublicationsPage')
