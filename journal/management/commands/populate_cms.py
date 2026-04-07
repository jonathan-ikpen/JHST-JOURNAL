from django.core.management.base import BaseCommand
from journal.models import Page, PageSection

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
                content='<p class="mb-6 text-lg"><strong>Journal of Hydrocarbon Science and Technology (JHST)</strong> is the official journal of the Petroleum Training Institute (PTI), Effurun, Nigeria. It is a premier open-access, peer-reviewed journal dedicated to disseminating high-quality research, technical innovations, and policy analyses in the energy sector.</p>',
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
                content='<ul class="list-disc pl-5 space-y-2"><li>To publish cutting-edge hypothesis-driven original research, review articles, and technical notes.</li><li>To bridge the gap between theoretical research and practical industrial application.</li><li>To inform policy and decision-making in the energy sector through rigorous scientific analysis.</li><li>To support the professional development of scientists, engineers, and researchers in the hydrocarbon field.</li></ul>',
                location='main',
                order=4
            )
            # Sidebar for About
            PageSection.objects.create(
                page=about_page,
                section_title='Information',
                content='''<ul class="space-y-2">
                    <li><a class="text-primary hover:underline" href="/subscription-advertising/">For Readers</a></li>
                    <li><a class="text-primary hover:underline" href="/author-guidelines/">For Authors</a></li>
                    <li><a class="text-primary hover:underline" href="/subscription-advertising/">For Librarians</a></li>
                </ul>''',
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
                content='<div class="mb-8"><p>The <strong>Journal of Hydrocarbon Science and Technology (JHST)</strong> is a peer-reviewed, open-access journal dedicated to the dissemination of high-quality research in the field of hydrocarbon science, energy technology, and related disciplines.</p></div>',
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
                content='''<p class="mb-4">JHST welcomes original research articles, technical notes, and review papers in the following areas, though not limited to:</p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <ul class="list-disc pl-5 space-y-2">
                    <li>Petroleum Geology and Geophysics</li>
                    <li>Reservoir Engineering and Simulation</li>
                    <li>Drilling and Completion Technology</li>
                    <li>Production Engineering and Optimization</li>
                    <li>Natural Gas Engineering and Processing</li>
                    <li>Petrochemicals and Refining Technology</li>
                  </ul>
                  <ul class="list-disc pl-5 space-y-2">
                    <li>Health, Safety, and Environment (HSE) in Energy</li>
                    <li>Energy Economics and Policy</li>
                    <li>Renewable Energy Integration with Hydrocarbons</li>
                    <li>Carbon Capture, Utilization, and Storage (CCUS)</li>
                    <li>Digital Transformation in Oil & Gas (AI, IoT)</li>
                    <li>Pipeline Engineering and Flow Assurance</li>
                  </ul>
                </div>''',
                location='main',
                order=3
            )

        # Guidelines Page
        guidelines_page, created = Page.objects.get_or_create(
            slug='guidelines',
            defaults={
                'title': 'Guidelines',
                'template_name': 'journal/guidelines.html'
            }
        )
        if created:
            PageSection.objects.create(
                page=guidelines_page,
                content='<p class="mb-6 text-lg">Please select the appropriate guidelines from the sections below:</p>',
                location='main',
                order=1
            )

        # Home Page
        home_page, created = Page.objects.get_or_create(
            slug='home',
            defaults={
                'title': 'Home',
                'template_name': 'journal/index.html'
            }
        )
        # Always update home page sections
        PageSection.objects.filter(page=home_page).delete()
        
        # Main Content
        PageSection.objects.create(
            page=home_page,
            section_title='An Introduction to the Journal',
            content='''<div style="padding: 56.25% 0 0 0; position: relative">
              <iframe
                src="https://player.vimeo.com/video/1129153382?byline=0&title=0&portrait=0&badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
                frameborder="0"
                allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
                referrerpolicy="strict-origin-when-cross-origin"
                style="
                  position: absolute;
                  top: 0;
                  left: 0;
                  width: 100%;
                  height: 100%;
                "
                title="JHST, PTI"
              ></iframe>
            </div>
            <script src="https://player.vimeo.com/api/player.js"></script>''',
            location='main',
            order=1
        )
        PageSection.objects.create(
            page=home_page,
            section_title='About the Journal',
            content='''<h3 class="font-bold text-lg mb-2">MISSION STATEMENT</h3>
            <p class="mb-4">Journal of Hydrocarbon Science and Technology (JHST) is the official publication of the Petroleum Training Institute, PTI, Effurun, Nigeria. The journal seeks to:</p>
            <ol class="list-decimal list-inside space-y-2 mb-6">
                <li>Provide a global platform for original, peer-reviewed research that deepens understanding and drives innovation across the hydrocarbon value chain — from exploration and production to refining, environmental management, renewable integration, and digital transformation</li>
                <li>Provide the general public with dynamic and required information to the world for the purpose of innovation, knowledge/education, lifestyle, culture and career development.</li>
            </ol>
            <h3 class="font-bold text-lg mb-4">JHST ORGANOGRAM</h3>
            <div class="space-y-4 relative pl-8">
                <div class="organogram-item">
                    <div class="organogram-number bg-[#00529B]">01</div>
                    <div class="organogram-content flex-1">
                        <div class="organogram-title bg-gray-200 dark:bg-gray-700 text-text-light dark:text-text-dark">Editor-in-Chief</div>
                        <div class="organogram-description border border-border-light dark:border-border-dark">Oversees the whole activities of JHST</div>
                    </div>
                </div>
                <div class="organogram-item">
                    <div class="organogram-number bg-[#B33A3A]">02</div>
                    <div class="organogram-content flex-1">
                        <div class="organogram-title bg-gray-200 dark:bg-gray-700 text-text-light dark:text-text-dark">Managing Editor</div>
                        <div class="organogram-description border border-border-light dark:border-border-dark">Coordinates journal's day-to-day activities, takes correspondences and make important suggestion on the acceptance or rejection of manuscripts to the editor-in-chief</div>
                    </div>
                </div>
                <div class="organogram-item">
                    <div class="organogram-number bg-[#34A853]">03</div>
                    <div class="organogram-content flex-1">
                        <div class="organogram-title bg-gray-200 dark:bg-gray-700 text-text-light dark:text-text-dark">Editorial Assistant</div>
                        <div class="organogram-description border border-border-light dark:border-border-dark">Supports the Managing Editor</div>
                    </div>
                </div>
                <div class="organogram-item">
                    <div class="organogram-number bg-[#4A90E2]">04</div>
                    <div class="organogram-content flex-1">
                        <div class="organogram-title bg-gray-200 dark:bg-gray-700 text-text-light dark:text-text-dark">Section Editor</div>
                        <div class="organogram-description border border-border-light dark:border-border-dark">Checks the appropriateness of a manuscript, handles peer-review and makes suggestions to the Managing Editor</div>
                    </div>
                </div>
                <div class="organogram-item">
                    <div class="organogram-number bg-[#795548]">05</div>
                    <div class="organogram-content flex-1">
                        <div class="organogram-title bg-gray-200 dark:bg-gray-700 text-text-light dark:text-text-dark">Editorial Board</div>
                        <div class="organogram-description border border-border-light dark:border-border-dark">Make all-inclusive advice to Editor-in-Chief and Managing Editor for better journal indices</div>
                    </div>
                </div>
            </div>''',
            location='main',
            order=2
        )
        PageSection.objects.create(
            page=home_page,
            section_title='From the Chief Editor’s Desk',
            content='''<p class="mb-4 leading-relaxed">In an era where the global energy landscape is undergoing unprecedented transformation, the Journal of Hydrocarbon Science and Technology (JHST) emerges as a timely response to a critical need — the need to rethink, redefine, and renew our approach to energy development, sustainability, and innovation...</p>
            <p class="mb-4 leading-relaxed">Our mission at JHST is to provide a global platform for original, peer-reviewed research that deepens understanding and drives innovation across the hydrocarbon value chain...</p>
            <p class="font-semibold text-primary">Dr. Fredrick B. Owoyemi</p>
            <p class="text-sm text-gray-600 dark:text-gray-400">Chief Editor, JHST</p>''',
            location='main',
            order=3
        )
        
        # Sidebar for Home
        PageSection.objects.create(
            page=home_page,
            section_title='New Release',
            content='<!-- The image will be uploaded in the Image field in Admin -->',
            location='sidebar',
            order=1
        )
        PageSection.objects.create(
            page=home_page,
            section_title='Information',
            content='''<ul class="space-y-2">
                <li><a class="text-primary hover:underline" href="/subscription-advertising/">For Readers</a></li>
                <li><a class="text-primary hover:underline" href="/author-guidelines/">For Authors</a></li>
                <li><a class="text-primary hover:underline" href="/subscription-advertising/">For Librarians</a></li>
            </ul>''',
            location='sidebar',
            order=2
        )
        PageSection.objects.create(
            page=home_page,
            section_title='Keywords',
            content='''<img alt="Keyword cloud" class="w-full" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC5EJmNcrMokICbf18WhpAWV1LPVCVZNabSXwWT62i35I9vEqXVaeZTNfCjpIYS0chgeLZQK-2YwQmOYLTxfWUtvCxHBgEDoesSPUohe8bpFkKAvIwgs81nJEgNwOvorT8qE74ZE1oHdV2vVW5yUPhohtF0vOeJ3InN-2vonPTD3hC8HaBMI17cM6WrFnckaOVIsZPFQaWJ1l8Em7zC4A_0QdYLkmj2elGbmUkdnvCRRSqBvdBt2773vVPEo-J8bBGam9U6_E9v76Lf" />''',
            location='sidebar',
            order=3
        )

        # Other informational pages
        slugs = [
            ('editorial-team', 'Editorial Team', 'journal/editorial_team.html'),
            ('publication-schedule', 'Publication Schedule', 'journal/page.html'),
            ('publication-fees', 'Publication Fees', 'journal/page.html'),
            ('contact', 'Contact Us', 'journal/page.html'),
            ('publications', 'Publications', 'journal/page.html'),
            ('indexing', 'Indexing', 'journal/page.html'),
            ('metrics', 'Metrics', 'journal/page.html'),
            ('author-guidelines', "Author's Guidelines", 'journal/page.html'),
            ('reviewer-guidelines', "Reviewer's Guidelines", 'journal/page.html'),
            ('ethics-malpractice', 'Ethics & Malpractice', 'journal/page.html'),
            ('open-access-policy', 'Open Access Policy', 'journal/page.html'),
            ('editorial-policy', 'Editorial Policy', 'journal/page.html'),
            ('peer-review-policy', 'Peer Review Policy', 'journal/page.html'),
            ('archiving-policy', 'Archiving Policy', 'journal/page.html'),
            ('subscription-advertising', 'Subscription & Advertising', 'journal/page.html'),
            ('plagiarism-policy', 'Plagiarism Policy', 'journal/page.html'),
            ('policies', 'Policies', 'journal/page.html'),
            ('jhst-journals', 'JHST Journals', 'journal/page.html'),
        ]
        for slug, title, template in slugs:
            Page.objects.get_or_create(
                slug=slug,
                defaults={'title': title, 'template_name': template}
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated initial CMS content'))
