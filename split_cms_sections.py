"""
Migration script: Splits each page's single 'main_content' blob into
individual named section keys with rich-text content per section.
Run once: python split_cms_sections.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()

from journal.models import Page, PageSection

def create(page_slug, key, text, order):
    page = Page.objects.get(slug=page_slug)
    PageSection.objects.update_or_create(
        page=page, section_key=key,
        defaults=dict(content_type='html', text_content=text, order=order)
    )
    print(f"  [{page_slug}] {key} -> saved")

# ─────────────────────────────────────────────
# ABOUT  (slug='about')
# ─────────────────────────────────────────────
Page.objects.filter(slug='about').update()
PageSection.objects.filter(page__slug='about', section_key='main_content').delete()

create('about', 'intro', """<p class="mb-6 text-lg">
<strong>Journal of Hydrocarbon Science and Technology (JHST)</strong> is
the official journal of the Petroleum Training Institute (PTI), Effurun,
Nigeria. It is a premier open-access, peer-reviewed journal dedicated to
disseminating high-quality research, technical innovations, and policy
analyses in the energy sector.
</p>""", 1)

create('about', 'mission_vision', """<div class="grid grid-cols-1 md:grid-cols-2 gap-8 my-10">
<div class="mb-4">
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80 inline-block">Our Mission</h2>
<div class="bg-primary/5 p-6 rounded border border-primary/10 h-full">
<p>To provide a global platform for the exchange of knowledge between academia and the hydrocarbon industry, fostering innovation and sustainable development in energy technologies.</p>
</div>
</div>
<div class="mb-4">
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80 inline-block">Our Vision</h2>
<div class="bg-primary/5 p-6 rounded border border-primary/10 h-full">
<p>To be a leading authoritative source of scientific and technical information for the global oil, gas, and energy community.</p>
</div>
</div>
</div>""", 2)

create('about', 'objectives', """<div class="mb-10">
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80">Objectives</h2>
<ul class="list-disc pl-5 space-y-2">
<li>To publish cutting-edge hypothesis-driven original research, review articles, and technical notes.</li>
<li>To bridge the gap between theoretical research and practical industrial application.</li>
<li>To inform policy and decision-making in the energy sector through rigorous scientific analysis.</li>
<li>To support the professional development of scientists, engineers, and researchers in the hydrocarbon field.</li>
</ul>
</div>""", 3)

create('about', 'explore_links', """<p class="mb-4">For more specific information, please explore the following sections:</p>
<ul class="grid grid-cols-1 sm:grid-cols-2 gap-4 list-none pl-0">
<li><a class="flex items-center text-primary font-semibold hover:underline" href="/aim-scope/"><span class="material-icons mr-2 text-sm">arrow_forward</span> Aim &amp; Scope</a></li>
<li><a class="flex items-center text-primary font-semibold hover:underline" href="/editorial-team/"><span class="material-icons mr-2 text-sm">arrow_forward</span> Editorial Team</a></li>
<li><a class="flex items-center text-primary font-semibold hover:underline" href="/publication-schedule/"><span class="material-icons mr-2 text-sm">arrow_forward</span> Publication Schedule</a></li>
<li><a class="flex items-center text-primary font-semibold hover:underline" href="/publication-fees/"><span class="material-icons mr-2 text-sm">arrow_forward</span> Publication Fees</a></li>
<li><a class="flex items-center text-primary font-semibold hover:underline" href="/contact/"><span class="material-icons mr-2 text-sm">arrow_forward</span> Contact Us</a></li>
</ul>""", 4)

# ─────────────────────────────────────────────
# AIM & SCOPE  (slug='aim-scope')
# ─────────────────────────────────────────────
PageSection.objects.filter(page__slug='aim-scope', section_key='main_content').delete()

create('aim-scope', 'intro', """<p>The <strong>Journal of Hydrocarbon Science and Technology (JHST)</strong>
is a peer-reviewed, open-access journal dedicated to the dissemination of high-quality
research in the field of hydrocarbon science, energy technology, and related disciplines.</p>""", 1)

create('aim-scope', 'aim', """<div class="mb-10">
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80">Aim</h2>
<p>Our primary aim is to provide a global platform for scientists, engineers, academicians, and industry
professionals to share their innovative research findings, technical advancements, and reviews. We strive to
bridge the gap between theoretical research and industrial application in the oil and gas sector.</p>
</div>""", 2)

create('aim-scope', 'scope', """<div class="mb-10">
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80">Scope</h2>
<p class="mb-4">JHST welcomes original research articles, technical notes, and review papers in the following areas, though not limited to:</p>
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
<li>Digital Transformation in Oil &amp; Gas (AI, IoT)</li>
<li>Pipeline Engineering and Flow Assurance</li>
</ul>
</div>
</div>""", 3)

# ─────────────────────────────────────────────
# EDITORIAL TEAM  (slug='editorial-team')
# ─────────────────────────────────────────────
PageSection.objects.filter(page__slug='editorial-team', section_key='main_content').delete()

create('editorial-team', 'editor_in_chief', """<div class="text-center mb-10">
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-6 pb-2 border-b-4 border-primary/80 inline-block">Editor-in-Chief</h2>
<div class="max-w-2xl bg-primary/5 p-8 rounded-lg border border-primary/20 mx-auto text-left">
<h3 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">Professor A. B. Johnson</h3>
<p class="text-lg text-gray-600 dark:text-gray-400">Department of Petroleum Engineering</p>
<p class="text-lg text-gray-600 dark:text-gray-400 mb-4">Petroleum Training Institute, Effurun, Nigeria</p>
<p class="text-gray-700 dark:text-gray-300 text-sm italic mb-4">Professor Johnson has over 30 years of experience in hydrocarbon research and academia.</p>
<a class="text-primary font-bold hover:underline inline-block" href="mailto:eic@jhst.org">eic@jhst.org</a>
</div>
</div>""", 1)

create('editorial-team', 'managing_editor', """<div class="mb-10">
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80">Managing Editor</h2>
<p class="text-sm text-gray-600 dark:text-gray-400 mb-4 italic">Oversees the journal's daily editorial operations and coordinates editorial workflow.</p>
<div>
<h3 class="font-bold text-lg text-gray-900 dark:text-gray-100">Dr. C. D. Okafor</h3>
<p class="text-gray-600 dark:text-gray-400 mb-2">Department of Chemical Engineering, PTI Effurun</p>
<a class="text-primary text-sm hover:underline block mt-1" href="mailto:managing.editor@jhst.org">managing.editor@jhst.org</a>
</div>
</div>""", 2)

create('editorial-team', 'editorial_assistant', """<div class="mb-10">
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80">Editorial Assistant</h2>
<p class="text-sm text-gray-600 dark:text-gray-400 mb-4 italic">Provides operational and editorial support to the Managing Editor.</p>
<div>
<h3 class="font-bold text-lg text-gray-900 dark:text-gray-100">Ms. J. K. Bello</h3>
<p class="text-gray-600 dark:text-gray-400 mb-2">Journal of Hydrocarbon Science and Technology</p>
<a class="text-primary text-sm hover:underline block mt-1" href="mailto:admin@jhst.org">admin@jhst.org</a>
</div>
</div>""", 3)

create('editorial-team', 'section_editors', """<div class="mb-10">
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80">Section Editors</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
<div>
<h3 class="font-bold text-gray-900 dark:text-gray-100">Prof. E. F. Mensah</h3>
<p class="text-gray-600 dark:text-gray-400 mb-2">Kwame Nkrumah University of Science and Technology, Ghana</p>
</div>
<div>
<h3 class="font-bold text-gray-900 dark:text-gray-100">Dr. G. H. Smith</h3>
<p class="text-gray-600 dark:text-gray-400 mb-2">University of Aberdeen, United Kingdom</p>
</div>
<div>
<h3 class="font-bold text-gray-900 dark:text-gray-100">Prof. I. J. Ahmed</h3>
<p class="text-gray-600 dark:text-gray-400 mb-2">University of Lagos, Nigeria</p>
</div>
<div>
<h3 class="font-bold text-gray-900 dark:text-gray-100">Dr. K. L. Wong</h3>
<p class="text-gray-600 dark:text-gray-400 mb-2">Universiti Teknologi PETRONAS, Malaysia</p>
</div>
</div>
</div>""", 4)

create('editorial-team', 'editorial_board', """<div>
<h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80">Editorial Board</h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
<div class="bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">
<span class="font-bold block text-gray-900 dark:text-gray-100">Prof. M. N. Opara</span>
<span class="text-gray-600 dark:text-gray-400 block mb-2 text-sm">Texas A&amp;M University, USA</span>
</div>
<div class="bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">
<span class="font-bold block text-gray-900 dark:text-gray-100">Prof. P. Q. Roy</span>
<span class="text-gray-600 dark:text-gray-400 block mb-2 text-sm">Indian Institute of Technology, India</span>
</div>
<div class="bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">
<span class="font-bold block text-gray-900 dark:text-gray-100">Dr. S. T. Utomi</span>
<span class="text-gray-600 dark:text-gray-400 block mb-2 text-sm">Shell Research Centre, Netherlands</span>
</div>
</div>
</div>""", 5)

# ─────────────────────────────────────────────
# GUIDELINES  (slug='guidelines')
# ─────────────────────────────────────────────
PageSection.objects.filter(page__slug='guidelines', section_key='main_content').delete()

create('guidelines', 'intro', """<p class="mb-6 text-lg">Please select the appropriate guidelines from the sections below:</p>""", 1)

create('guidelines', 'guideline_cards', """<div class="grid grid-cols-1 md:grid-cols-2 gap-8 my-8">
<a class="block group bg-primary/5 p-8 rounded border border-primary/10 hover:bg-primary/10 transition" href="/author-guidelines/">
<div class="flex items-center mb-4">
<span class="material-icons text-4xl text-primary mr-4">description</span>
<h2 class="text-2xl font-bold text-primary group-hover:underline">Author's Guidelines</h2>
</div>
<p class="text-gray-700 dark:text-gray-300">Comprehensive instructions for manuscript preparation, formatting, submission requirements, and information on publication fees.</p>
</a>
<a class="block group bg-primary/5 p-8 rounded border border-primary/10 hover:bg-primary/10 transition" href="/reviewer-guidelines/">
<div class="flex items-center mb-4">
<span class="material-icons text-4xl text-primary mr-4">rate_review</span>
<h2 class="text-2xl font-bold text-primary group-hover:underline">Reviewer's Guidelines</h2>
</div>
<p class="text-gray-700 dark:text-gray-300">Information for peer reviewers regarding confidentiality, evaluation criteria, report structure, and benefits.</p>
</a>
</div>""", 2)

# ─────────────────────────────────────────────
# AUTHOR GUIDELINES  (slug='author-guidelines')
# Splits the 20+ subsections each to their own section key
# ─────────────────────────────────────────────
PageSection.objects.filter(page__slug='author-guidelines', section_key='main_content').delete()

author_sections = [
    ('about_journal', 'About the Journal', """<p>The Journal of Hydrocarbon Science and Technology (JHST), the official journal of the Petroleum Training Institute (PTI), Effurun, Nigeria, is dedicated to publishing high-quality, peer-reviewed, and hypothesis-driven original research across all disciplines of hydrocarbon science and technology.</p>"""),
    ('open_access', 'Open Access Policy', """<p>This journal ensures immediate open access to its content. Authors retain full copyright over their work while granting first publication rights to JHST. All articles are published under the <strong>CC BY 4.0</strong> license.</p>"""),
    ('publication_schedule', 'Publication Schedule', """<p>JHST publishes two issues per year and ensures that manuscripts are made available online as soon as they are accepted.</p>"""),
    ('editorial_policy', 'Editorial Policy', """<p>Authors must prepare their manuscripts following the Instructions for Authors. The Journal reserves the right to make formal changes and language corrections necessary in a manuscript accepted for publication.</p>"""),
    ('general_requirements', 'General Requirements', """<p>All submitted manuscripts should contain original research written in English, not previously published and not under consideration elsewhere. Manuscripts may be submitted as original papers or short communications.</p>"""),
    ('manuscript_preparation', 'Manuscript Preparation', """<p>The manuscript must be typed in 12-point font, double-spaced on A4 paper with margins of 1 inch on all sides. All pages should be page-numbered.</p>"""),
    ('cover_letter', 'Cover Letter', """<p>The cover letter must clearly show full contact details of the corresponding author with postal address, phone numbers and e-mail address. The relevance of the study should also be indicated. A minimum of three (3) potential reviewers with email addresses should be suggested.</p>"""),
    ('title_page', 'Title Page', """<p>The title page should contain the title of the manuscript, the authors' names, affiliations and email addresses. <strong>All authors are required to provide their 16-digit ORCID iD.</strong> One of the authors should be designated as the corresponding author.</p>"""),
    ('abstract', 'Abstract', """<p>Abstract should not be more than 250 words, containing a concise summary of the objective and scope, general methods, results, conclusion and significance of the research.</p>"""),
    ('keywords', 'Keywords', """<p>A maximum of six keywords. Words appearing in the title should not be given as keywords. Keywords must correspond with Medical Subject Headings (MESH) where applicable.</p>"""),
    ('introduction', 'Introduction', """<p>The Introduction should provide sufficient background on the study, the statement of the problem, and the rationale for conducting the research. The aim should also be clearly defined.</p>"""),
    ('materials_methods', 'Materials and Methods', """<p>This section must provide sufficient detail to allow the work to be reproduced. Methods already published should be indicated by reference. The type of statistical tool(s) used must be mentioned and justified.</p>"""),
    ('results_discussion', 'Results and Discussion', """<p>Authors may wish to combine the two sections (Results and Discussion).</p>"""),
    ('conclusion', 'Conclusion', """<p>The conclusion must reflect the judgment or decision reached by reasoning after the discussion. This section sums up the arguments about what you have been writing about.</p>"""),
    ('acknowledgements', 'Acknowledgements', """<p>Major contributors who did not qualify as authors should be acknowledged accordingly. Funding sources should also be acknowledged appropriately.</p>"""),
    ('conflict_of_interest', 'Conflict(s) of Interests', """<p>Authors are required to disclose financial interests in any company or institution that might benefit from their publication. The statement should be placed directly following the Acknowledgements.</p>"""),
    ('references', 'References', """<p class="mb-4">All references must be listed at the end of the paper in Vancouver Reference Format, numbered consecutively in order of appearance. Authors are responsible for ensuring accuracy.</p>
<div class="space-y-4 text-sm bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">
<p><strong>Books:</strong> Author(s). <em>Title of book</em>. Edition. Place: Publisher; Year.</p>
<p><strong>Journal Articles:</strong> Author(s). Title of article. <em>Abbreviated Journal Title</em>. Year; Volume(Issue): page numbers.</p>
<p><strong>Webpages:</strong> Author(s). Title. [Internet]. Place: Publisher; Date [cited Date]. Available from: URL</p>
</div>"""),
    ('submission', 'Submission', """<p>This should be done <strong>ONLY</strong> online at the journal website. Submission through any other means will not be processed.</p>"""),
    ('assessment', 'Assessment', """<p>Each manuscript will be subjected to both plagiarism check and preliminary editorial review before it can be sent for double-blind peer review. Acceptance will be based on originality of the research and contribution to scientific knowledge.</p>"""),
    ('publication_fees', 'Publication Fees', """<p>An article publication fee of Thirty Thousand Naira only (₦30,000.00) or One Hundred Dollars (100 USD) will be charged on any article accepted for publication. Payment details will be provided upon acceptance.</p>"""),
    ('checklist', 'Submission Preparation Checklist', """<ul class="list-disc pl-5 space-y-2">
<li>The manuscript has not been previously published nor under consideration by another journal.</li>
<li>The manuscript file is in OpenOffice, Microsoft Word, RTF or WordPerfect document format.</li>
<li>The text is double-spaced; uses a 12-point font; employs italics, rather than underlining.</li>
<li>All illustrations, figures, and tables are placed within the text at the appropriate points.</li>
<li>A declaration statement on conflict of interest.</li>
<li>A cover letter stating the novelty and significance of the work, and a list of at least three suggested reviewers.</li>
</ul>"""),
]

for i, (key, title, content) in enumerate(author_sections, start=1):
    html = f'<div class="mb-10"><h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 pb-2 border-b-4 border-primary/80">{title}</h2>{content}</div>'
    create('author-guidelines', key, html, i)

print("\nAll sections split successfully!")
print("Now run: python dump_fixture.py && python manage.py setup_cms")
