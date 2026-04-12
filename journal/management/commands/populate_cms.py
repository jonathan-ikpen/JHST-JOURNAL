from django.core.management.base import BaseCommand
from journal.models import Page, PageSection, OrganogramItem

class Command(BaseCommand):
    help = 'Populate initial CMS content from static templates'

    def handle(self, *args, **options):
        # About Page
        about_page, created = Page.objects.get_or_create(
            slug='about',
            defaults={
                'title': 'About the Journal',
                'template_name': 'journal/about.html'
            }
        )
        if created:
            PageSection.objects.create(
                page=about_page,
                content='<p><strong>Journal of Hydrocarbon Science and Technology (JHST)</strong> is the official journal of the Petroleum Training Institute (PTI), Effurun, Nigeria. It is a premier open-access, peer-reviewed journal dedicated to disseminating high-quality research, technical innovations, and policy analyses in the energy sector.</p>',
                location='main',
                order=1
            )
            PageSection.objects.create(
                page=about_page,
                section_title='Our Mission',
                content='<p>To provide a global platform for the exchange of knowledge between academia and the hydrocarbon industry, fostering innovation and sustainable development in energy technologies.</p>',
                location='main',
                order=2
            )
            PageSection.objects.create(
                page=about_page,
                section_title='Our Vision',
                content='<p>To be a leading authoritative source of scientific and technical information for the global oil, gas, and energy community.</p>',
                location='main',
                order=3
            )
            PageSection.objects.create(
                page=about_page,
                section_title='Objectives',
                content='<ul><li>To publish cutting-edge hypothesis-driven original research, review articles, and technical notes.</li><li>To bridge the gap between theoretical research and practical industrial application.</li><li>To inform policy and decision-making in the energy sector through rigorous scientific analysis.</li><li>To support the professional development of scientists, engineers, and researchers in the hydrocarbon field.</li></ul>',
                location='main',
                order=4
            )
            # Sidebar for About
            PageSection.objects.create(
                page=about_page,
                section_title='Information',
                content='<ul><li><a href="/subscription-advertising/">For Readers</a></li><li><a href="/author-guidelines/">For Authors</a></li><li><a href="/subscription-advertising/">For Librarians</a></li></ul>',
                location='sidebar',
                order=1
            )

        # Aim & Scope Page
        aim_page, created = Page.objects.get_or_create(
            slug='aim-scope',
            defaults={
                'title': 'Aim & Scope',
                'template_name': 'journal/aim_scope.html'
            }
        )
        if created:
            PageSection.objects.create(
                page=aim_page,
                content='<p>The <strong>Journal of Hydrocarbon Science and Technology (JHST)</strong> is a peer-reviewed, open-access journal dedicated to the dissemination of high-quality research in the field of hydrocarbon science, energy technology, and related disciplines.</p>',
                location='main',
                order=1
            )
            PageSection.objects.create(
                page=aim_page,
                section_title='Aim',
                content='<p>Our primary aim is to provide a global platform for scientists, engineers, academicians, and industry professionals to share their innovative research findings, technical advancements, and reviews. We strive to bridge the gap between theoretical research and industrial application in the oil and gas sector.</p>',
                location='main',
                order=2
            )
            PageSection.objects.create(
                page=aim_page,
                section_title='Scope',
                section_type='GRID',
                content='''<p>JHST welcomes original research articles, technical notes, and review papers in the following areas, though not limited to:</p>
                <ul>
                    <li>Petroleum Geology and Geophysics</li>
                    <li>Reservoir Engineering and Simulation</li>
                    <li>Drilling and Completion Technology</li>
                    <li>Production Engineering and Optimization</li>
                    <li>Natural Gas Engineering and Processing</li>
                    <li>Petrochemicals and Refining Technology</li>
                </ul>
                <ul>
                    <li>Health, Safety, and Environment (HSE) in Energy</li>
                    <li>Energy Economics and Policy</li>
                    <li>Renewable Energy Integration with Hydrocarbons</li>
                    <li>Carbon Capture, Utilization, and Storage (CCUS)</li>
                    <li>Digital Transformation in Oil & Gas (AI, IoT)</li>
                    <li>Pipeline Engineering and Flow Assurance</li>
                </ul>''',
                location='main',
                order=3
            )

        # Home Page
        home_page, created = Page.objects.get_or_create(
            slug='home',
            defaults={
                'title': 'Home',
                'template_name': 'journal/index.html'
            }
        )
        # Always update home page sections to ensure data integrity
        PageSection.objects.filter(page=home_page).delete()
        
        # Main Content
        PageSection.objects.create(
            page=home_page,
            section_title='An Introduction to the Journal',
            section_type='VIDEO',
            vimeo_url='https://vimeo.com/1129153382',
            location='main',
            order=1
        )
        
        organogram_section = PageSection.objects.create(
            page=home_page,
            section_title='About the Journal',
            section_type='ORGANOGRAM',
            content='''<h3>MISSION STATEMENT</h3>
            <p>Journal of Hydrocarbon Science and Technology (JHST) is the official publication of the Petroleum Training Institute, PTI, Effurun, Nigeria. The journal seeks to:</p>
            <ol>
                <li>Provide a global platform for original, peer-reviewed research that deepens understanding and drives innovation across the hydrocarbon value chain</li>
                <li>Provide the general public with dynamic and required information to the world for the purpose of innovation, knowledge/education, lifestyle, culture and career development.</li>
            </ol>
            <h3>JHST ORGANOGRAM</h3>''',
            location='main',
            order=2
        )
        
        # Create Organogram Items
        OrganogramItem.objects.create(
            section=organogram_section,
            number='01',
            title='Editor-in-Chief',
            description='Oversees the whole activities of JHST',
            color_code='#00529B',
            order=1
        )
        OrganogramItem.objects.create(
            section=organogram_section,
            number='02',
            title='Managing Editor',
            description="Coordinates journal's day-to-day activities and makes suggestions on manuscript acceptance/rejection",
            color_code='#B33A3A',
            order=2
        )
        OrganogramItem.objects.create(
            section=organogram_section,
            number='03',
            title='Editorial Assistant',
            description='Supports the Managing Editor',
            color_code='#34A853',
            order=3
        )
        OrganogramItem.objects.create(
            section=organogram_section,
            number='04',
            title='Section Editor',
            description='Checks manuscript appropriateness and handles peer-review',
            color_code='#4A90E2',
            order=4
        )
        OrganogramItem.objects.create(
            section=organogram_section,
            number='05',
            title='Editorial Board',
            description='Makes all-inclusive advice for better journal indices',
            color_code='#795548',
            order=5
        )

        PageSection.objects.create(
            page=home_page,
            section_title='From the Chief Editor’s Desk',
            content='''<p>In an era where the global energy landscape is undergoing unprecedented transformation, the Journal of Hydrocarbon Science and Technology (JHST) emerges as a timely response to a critical need...</p>
            <p><strong>Dr. Fredrick B. Owoyemi</strong><br>Chief Editor, JHST</p>''',
            location='main',
            order=3
        )
        
        # Sidebar for Home
        PageSection.objects.create(
            page=home_page,
            section_title='New Release',
            content='',
            location='sidebar',
            order=1
        )
        PageSection.objects.create(
            page=home_page,
            section_title='Information',
            content='<ul><li><a href="/subscription-advertising/">For Readers</a></li><li><a href="/author-guidelines/">For Authors</a></li><li><a href="/subscription-advertising/">For Librarians</a></li></ul>',
            location='sidebar',
            order=2
        )
        PageSection.objects.create(
            page=home_page,
            section_title='Keywords',
            content='<img alt="Keywords" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC5EJmNcrMokICbf18WhpAWV1LPVCVZNabSXwWT62i35I9vEqXVaeZTNfCjpIYS0chgeLZQK-2YwQmOYLTxfWUtvCxHBgEDoesSPUohe8bpFkKAvIwgs81nJEgNwOvorT8qE74ZE1oHdV2vVW5yUPhohtF0vOeJ3InN-2vonPTD3hC8HaBMI17cM6WrFnckaOVIsZPFQaWJ1l8Em7zC4A_0QdYLkmj2elGbmUkdnvCRRSqBvdBt2773vVPEo-J8bBGam9U6_E9v76Lf" />',
            location='sidebar',
            order=3
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated initial CMS content'))
