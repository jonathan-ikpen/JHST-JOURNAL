import re

file_path = r'c:\jojo\school\jhst-journal\pages\management\commands\populate_pages.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update Home Page
home_page_replace = """    def _populate_home_page(self):
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
                'In an era where the global energy landscape is undergoing unprecedented transformation, the Journal of '
                'Hydrocarbon Science and Technology (JHST) emerges as a timely response to a critical need — the need '
                'to rethink, redefine, and renew our approach to energy development, sustainability, and innovation. '
                'The Petroleum Training Institute (PTI), for over five decades, has served as Nigeria’s premier institution '
                'for technical excellence in the petroleum and allied sectors. Through education, applied research, and '
                'industry collaboration, PTI has equipped generations of professionals with the competence and creativity '
                'to advance the oil and gas industry. The JHST is a natural evolution of this legacy — a bridge between '
                'research and real-world application, between academia and industry, between innovation and impact.'
            ),
            'chief_editor_para_2': (
                'Our mission at JHST is to provide a global platform for original, peer-reviewed research that deepens '
                'understanding and drives innovation across the hydrocarbon value chain — from exploration and production '
                'to refining, environmental management, renewable integration, and digital transformation. We welcome '
                'contributions that address both the opportunities and the challenges of the energy transition — where '
                'hydrocarbons, renewables, and new technologies converge to shape a sustainable future.'
            ),
            'chief_editor_para_3': (
                'In line with PTI’s commitment to excellence, JHST upholds rigorous standards of scholarly integrity, '
                'transparency, and quality. Our distinguished editorial and review boards bring together leading experts, '
                'scientists, and professionals from around the world — ensuring that each publication meets the highest '
                'levels of technical and ethical credibility. We envision this Journal not merely as a collection of articles, '
                'but as a platform for dialogue, a catalyst for innovation, and a repository of insight — where ideas '
                'transform into technologies, and research drives resilience in an evolving energy economy.'
            ),
            'chief_editor_para_4': (
                'As we embark on this exciting journey, I invite researchers, industry professionals, policymakers, and '
                'students alike to contribute, collaborate, and engage with JHST. Together, we can advance the science '
                'and technology that sustain our energy future — responsibly, intelligently, and inclusively. Welcome '
                'to the Journal of Hydrocarbon Science and Technology — where energy meets innovation.'
            ),
            'chief_editor_name': 'Dr. Fredrick B. Owoyemi',
            'chief_editor_role': 'Chief Editor, Journal of Hydrocarbon Science and Technology (JHST)',
        })
        self.stdout.write('  OK HomePage')"""

content = re.sub(r'    def _populate_home_page\(self\):.*?self\.stdout\.write\(\'  OK HomePage\'\)', home_page_replace, content, flags=re.DOTALL)

# Update Contact Page
contact_page_replace = """    def _populate_contact_page(self):
        ContactPage.objects.update_or_create(pk=1, defaults={
            'office_journal_name': 'Journal of Hydrocarbon Science and Technology',
            'office_department': 'Directorate of Research and Development',
            'office_institution': 'Petroleum Training Institute',
            'office_address_line1': 'P.M.B. 20, Effurun',
            'office_address_line2': 'Delta State, Nigeria.',
            'principal_name': 'Dr. Fredrick B. Owoyemi',
            'principal_role': 'Editor-in-Chief',
            'principal_email': 'eic@jhst.org',
            'principal_phone': '+234 800 123 4567',
            'support_name': 'Tech Support Team',
            'support_role': 'For technical issues with submission',
            'support_email': 'support@jhst.org',
        })
        self.stdout.write('  OK ContactPage')"""
content = re.sub(r'    def _populate_contact_page\(self\):.*?self\.stdout\.write\(\'  OK ContactPage\'\)', contact_page_replace, content, flags=re.DOTALL)

# Update Aim Scope
aim_scope_replace = """    def _populate_aim_scope_page(self):
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
                'Exploration, Production, and Operations (Upstream, Midstream, Downstream)\\n'
                'Health, Safety, and Environment (HSE) Management\\n'
                'Renewable Energy Integration Technologies\\n'
                'Transportation, Logistics, and Gas Flare Commercialization\\n'
                'Innovations in R&D, Digital Tech, and AI/Robotics\\n'
                'Asset Protection, SCADA, IoT, and Remote Monitoring\\n'
                'Energy Trading, Risk Management, and Financing\\n'
                'Sustainability, Environmental Management, and CCUS'
            ),
            'scope_col2': _ul(
                'Geology, Geophysics, and Mineral Exploration\\n'
                'Offshore, Marine, and Subsea Technology\\n'
                'Human Capital and Workforce Development\\n'
                'Regulatory, Legal, and Policy Frameworks\\n'
                'Market Trends and Strategic Outlook\\n'
                'Unconventional Resources and Energy Security\\n'
                'Collaboration and industry partnerships\\n'
                'Process Systems, Hydrocarbon Accounting and Management'
            ),
        })
        self.stdout.write('  OK AimScopePage')"""
content = re.sub(r'    def _populate_aim_scope_page\(self\):.*?self\.stdout\.write\(\'  OK AimScopePage\'\)', aim_scope_replace, content, flags=re.DOTALL)

# Update Editorial Team Page
team_page_replace = """    def _populate_editorial_team_page(self):
        EditorialTeamPage.objects.update_or_create(pk=1, defaults={
            'editor_in_chief_description': _p(
                'The Editor-in-Chief assumes primary responsibility for the journal’s scientific '
                'and editorial quality. He oversees the strategic direction, leads the editorial '
                'board, and ensures the journal maintains its core mission and ethical standards.'
            ),
            'managing_director_description': _p(
                'Oversees the day-to-day operations of the journal, coordinates the editorial '
                'workflow, manages correspondence, and assists the Editor-in-Chief in decisions '
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
            'advisory_board_description': _p(
                'The Advisory Board comprises distinguished academics and industry professionals '
                'who provide strategic counsel and insights to ensure the journal remains at the '
                'forefront of scientific research and industry trends.'
            ),
        })
        self.stdout.write('  OK EditorialTeamPage')"""
content = re.sub(r'    def _populate_editorial_team_page\(self\):.*?self\.stdout\.write\(\'  OK EditorialTeamPage\'\)', team_page_replace, content, flags=re.DOTALL)

# Read members generated list
with open(r'c:\jojo\school\jhst-journal\scratch_generate.txt', 'r', encoding='utf-8') as f:
    members_list = f.read()

team_members_replace = """    def _populate_team_members(self):
""" + members_list + """
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
        self.stdout.write(f'  OK TeamMembers ({len(members)})')"""
content = re.sub(r'    def _populate_team_members\(self\):.*?self\.stdout\.write\(f\'  OK TeamMembers \({len\(members\)}\)\'\)', team_members_replace, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done updating populate_pages.py")
