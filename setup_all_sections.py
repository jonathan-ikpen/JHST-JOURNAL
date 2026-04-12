"""
Comprehensive CMS section reset — matches EXACT headings from live jhst.org.
Headings are HARDCODED in templates. Only body paragraphs go in rich text fields.
Run: python setup_all_sections.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
django.setup()
from journal.models import Page, PageSection

def wipe(slug, *keep_keys):
    """Delete all sections for a page except the ones in keep_keys."""
    qs = PageSection.objects.filter(page__slug=slug)
    if keep_keys:
        qs = qs.exclude(section_key__in=keep_keys)
    qs.delete()

def s(page_slug, key, body, order=0):
    page = Page.objects.get(slug=page_slug)
    PageSection.objects.update_or_create(
        page=page, section_key=key,
        defaults=dict(content_type='html', text_content=body, order=order)
    )
    print(f"  [{page_slug}] {key}")

# ═══════════════════════════════════════════════════════════
# ABOUT  — Headings: Our Mission | Our Vision | Objectives
# ═══════════════════════════════════════════════════════════
wipe('about', 'intro','mission','vision','objectives')

s('about','intro',"""<p class="mb-4 text-lg"><strong>Journal of Hydrocarbon Science and Technology (JHST)</strong> is the official journal of the Petroleum Training Institute (PTI), Effurun, Nigeria. It is a premier open-access, peer-reviewed journal dedicated to disseminating high-quality research, technical innovations, and policy analyses in the energy sector.</p>""",1)

s('about','mission',"""<p>To provide a global platform for the exchange of knowledge between academia and the hydrocarbon industry, fostering innovation and sustainable development in energy technologies.</p>""",2)

s('about','vision',"""<p>To be a leading authoritative source of scientific and technical information for the global oil, gas, and energy community.</p>""",3)

s('about','objectives',"""<ul class="list-disc pl-5 space-y-2">
<li>To publish cutting-edge hypothesis-driven original research, review articles, and technical notes.</li>
<li>To bridge the gap between theoretical research and practical industrial application.</li>
<li>To inform policy and decision-making in the energy sector through rigorous scientific analysis.</li>
<li>To support the professional development of scientists, engineers, and researchers in the hydrocarbon field.</li>
</ul>""",4)

# ═══════════════════════════════════════════════════════════
# AIM & SCOPE  — Headings: Aim | Scope
# ═══════════════════════════════════════════════════════════
wipe('aim-scope','intro','aim','scope')

s('aim-scope','intro',"""<p>The <strong>Journal of Hydrocarbon Science and Technology (JHST)</strong> is a peer-reviewed, open-access journal dedicated to the dissemination of high-quality research in the field of hydrocarbon science, energy technology, and related disciplines.</p>""",1)

s('aim-scope','aim',"""<p>Our primary aim is to provide a global platform for scientists, engineers, academicians, and industry professionals to share their innovative research findings, technical advancements, and reviews. We strive to bridge the gap between theoretical research and industrial application in the oil and gas sector.</p>""",2)

s('aim-scope','scope',"""<p class="mb-4">JHST welcomes original research articles, technical notes, and review papers in the following areas, though not limited to:</p>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
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
</div>""",3)

# ═══════════════════════════════════════════════════════════
# EDITORIAL TEAM  — Headings: Editor-in-Chief | Managing Director |
#                   Editorial Assistant | Section Editors | Editorial Board
# ═══════════════════════════════════════════════════════════
wipe('editorial-team','editor_in_chief','managing_director','editorial_assistant','section_editors','editorial_board')

s('editorial-team','editor_in_chief',"""<div class="max-w-2xl bg-primary/5 p-8 rounded-lg border border-primary/20 mx-auto text-left">
<h3 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">Professor A. B. Johnson</h3>
<p class="text-lg text-gray-600 dark:text-gray-400">Department of Petroleum Engineering</p>
<p class="text-lg text-gray-600 dark:text-gray-400 mb-4">Petroleum Training Institute, Effurun, Nigeria</p>
<p class="text-gray-700 dark:text-gray-300 text-sm italic mb-4">Professor Johnson has over 30 years of experience in hydrocarbon research and academia, leading numerous groundbreaking studies in petroleum engineering and sustainable energy transition.</p>
<a class="text-primary font-bold hover:underline inline-block" href="mailto:eic@jhst.org">eic@jhst.org</a>
</div>""",1)

s('editorial-team','managing_director',"""<p class="text-sm text-gray-600 dark:text-gray-400 mb-4 italic">Oversees the journal's daily editorial operations, manages scholarly correspondence, and provides informed recommendations to the Editor-in-Chief regarding manuscript acceptance or rejection.</p>
<div>
<h3 class="font-bold text-lg text-gray-900 dark:text-gray-100">Dr. C. D. Okafor</h3>
<p class="text-gray-600 dark:text-gray-400 mb-2">Department of Chemical Engineering, PTI Effurun</p>
<a class="text-primary text-sm hover:underline block mt-1" href="mailto:managing.director@jhst.org">managing.director@jhst.org</a>
</div>""",2)

s('editorial-team','editorial_assistant',"""<p class="text-sm text-gray-600 dark:text-gray-400 mb-4 italic">Provides operational and editorial support to the Managing Director in the administration of journal activities.</p>
<div>
<h3 class="font-bold text-lg text-gray-900 dark:text-gray-100">Ms. J. K. Bello</h3>
<p class="text-gray-600 dark:text-gray-400 mb-2">Journal of Hydrocarbon Science and Technology</p>
<a class="text-primary text-sm hover:underline block mt-1" href="mailto:admin@jhst.org">admin@jhst.org</a>
</div>""",3)

s('editorial-team','section_editors',"""<p class="text-sm text-gray-600 dark:text-gray-400 mb-4 italic">Assesses the suitability of submitted manuscripts, manages the peer-review process, and submits informed recommendations to the Managing Director.</p>
<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
<div>
<h3 class="font-bold text-gray-900 dark:text-gray-100">Prof. E. F. Mensah</h3>
<p class="text-gray-600 dark:text-gray-400 text-sm">Kwame Nkrumah University of Science and Technology, Ghana</p>
</div>
<div>
<h3 class="font-bold text-gray-900 dark:text-gray-100">Dr. G. H. Smith</h3>
<p class="text-gray-600 dark:text-gray-400 text-sm">University of Aberdeen, United Kingdom</p>
</div>
<div>
<h3 class="font-bold text-gray-900 dark:text-gray-100">Prof. I. J. Ahmed</h3>
<p class="text-gray-600 dark:text-gray-400 text-sm">University of Lagos, Nigeria</p>
</div>
<div>
<h3 class="font-bold text-gray-900 dark:text-gray-100">Dr. K. L. Wong</h3>
<p class="text-gray-600 dark:text-gray-400 text-sm">Universiti Teknologi PETRONAS, Malaysia</p>
</div>
</div>""",4)

s('editorial-team','editorial_board',"""<p class="text-sm text-gray-600 dark:text-gray-400 mb-4 italic">Provides comprehensive strategic guidance to the Editor-in-Chief and Managing Director aimed at enhancing journal quality, visibility, and indexing performance.</p>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
<div class="bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">
<span class="font-bold block">Prof. M. N. Opara</span>
<span class="text-sm text-gray-500">Texas A&amp;M University, USA</span>
</div>
<div class="bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">
<span class="font-bold block">Prof. P. Q. Roy</span>
<span class="text-sm text-gray-500">Indian Institute of Technology, India</span>
</div>
<div class="bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">
<span class="font-bold block">Dr. S. T. Utomi</span>
<span class="text-sm text-gray-500">Shell Research Centre, Netherlands</span>
</div>
</div>""",5)

# ═══════════════════════════════════════════════════════════
# GUIDELINES HUB — No sub-headings (just cards)
# ═══════════════════════════════════════════════════════════
wipe('guidelines','intro','guideline_cards')

s('guidelines','intro',"""<p class="text-lg text-gray-700 dark:text-gray-300">Please select the appropriate guidelines from the sections below:</p>""",1)

s('guidelines','guideline_cards',"""<div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-6">
<a class="block group bg-primary/5 p-8 rounded border border-primary/10 hover:bg-primary/10 transition" href="/author-guidelines/">
<div class="flex items-center mb-4">
<span class="material-icons text-4xl text-primary mr-4">description</span>
<h2 class="text-2xl font-bold text-primary group-hover:underline">Author's Guideline</h2>
</div>
<p class="text-gray-700 dark:text-gray-300">Comprehensive instructions for manuscript preparation, formatting, submission requirements, and information on publication fees.</p>
</a>
<a class="block group bg-primary/5 p-8 rounded border border-primary/10 hover:bg-primary/10 transition" href="/reviewer-guidelines/">
<div class="flex items-center mb-4">
<span class="material-icons text-4xl text-primary mr-4">rate_review</span>
<h2 class="text-2xl font-bold text-primary group-hover:underline">Reviewer's Guideline</h2>
</div>
<p class="text-gray-700 dark:text-gray-300">Information for peer reviewers regarding confidentiality, evaluation criteria, report structure, and benefits.</p>
</a>
</div>""",2)

# ═══════════════════════════════════════════════════════════
# AUTHOR GUIDELINES — Headings from live site:
# About the Journal | Open Access and Copyright | Editorial Policy |
# General Requirements | Manuscript Preparation | Abstract | Keywords |
# Introduction | Materials and Methods | Discussion | Conclusion |
# Acknowledgements | Submission | Assessment | Publication Fees |
# Submission Preparation Checklist
# ═══════════════════════════════════════════════════════════
wipe('author-guidelines',
     'about_journal','open_access','editorial_policy','general_requirements',
     'manuscript_preparation','abstract','keywords','introduction',
     'materials_methods','discussion','conclusion','acknowledgements',
     'submission','assessment','publication_fees','checklist')

s('author-guidelines','about_journal',"""<p>The Journal of Hydrocarbon Science and Technology (JHST), the official journal of the Petroleum Training Institute (PTI), Effurun, Nigeria, is dedicated to publishing high-quality, peer-reviewed, and hypothesis-driven original research across all disciplines of hydrocarbon science and technology. JHST provides an inclusive platform for innovative research from diverse pure and applied sciences fields.</p>
<p class="mt-4">Since its inception, JHST has been recognised for its commitment to academic excellence. JHST is indexed and abstracted by Scopus, Directory of Open Access Journals (DOAJ), Google Scholar, and is actively pursuing inclusion in other major databases.</p>""",1)

s('author-guidelines','open_access',"""<p>This journal ensures immediate open access to its content, embracing the principle that freely available research fosters a broader global knowledge exchange. Authors retain full copyright over their work while granting first publication rights to JHST. All articles in JHST are published under the Creative Commons Attribution 4.0 International License (CC BY 4.0), allowing for unrestricted use, distribution, and reproduction, provided proper credit is given to the original authors and source.</p>""",2)

s('author-guidelines','editorial_policy',"""<p>Authors must prepare their manuscripts following the Instructions for Authors of the journal. Manuscripts that do not follow the format and style of the journal may be returned to the authors for revision or rejected. The Journal reserves the right to make any further formal changes and language corrections necessary in a manuscript accepted for publication. Manuscripts are accepted with the understanding that the authors have not violated the ethics of research and publishing during the conduct of the experiment and writing of the manuscript.</p>""",3)

s('author-guidelines','general_requirements',"""<p>All submitted manuscripts should contain original research written in the English Language, not previously published and not under consideration for publication elsewhere. Manuscripts may be submitted for consideration as original papers (research articles describing original experimental results) and short communications. The Journal also publishes mini-reviews, which are by invitation. However, authors willing to submit a review article may write a proposal for the editor-in-chief.</p>""",4)

s('author-guidelines','manuscript_preparation',"""<p>The manuscript (including references, tables, boxes, and legends) must be typed in 12-point font, double-spaced on A4 paper with margins of 1 inch or 4.5 cm on all sides. All pages in the manuscript should be page-numbered.</p>
<p class="mt-4">The <strong>cover letter</strong> must clearly show the full contact details with the corresponding author's postal address(es), phone numbers and e-mail address(es). A minimum of three (3) potential reviewers with their email addresses and institutions should be suggested.</p>
<p class="mt-4">The <strong>title page</strong> should contain the title of the manuscript, the authors' names, affiliations and email addresses. <strong>All authors are required to provide their 16-digit ORCID iD.</strong></p>""",5)

s('author-guidelines','abstract',"""<p>Abstract should not be more than 250 words, containing a concise summary of the objective and scope, general methods, results, conclusion and significance of the research.</p>""",6)

s('author-guidelines','keywords',"""<p>The journal welcomes a maximum of six keywords, which should be words that can be used to retrieve the paper, not general words. Words appearing in the title should not be given as keywords. The keywords must correspond with those in Medical Subject Headings (MESH) where applicable.</p>""",7)

s('author-guidelines','introduction',"""<p>The Introduction should provide sufficient background on the study. It should also give the statement of the problem and the rationale for conducting the research. The aim should also be clearly defined. The contribution to the area of study should be identified. All these must be presented in a logical manner.</p>""",8)

s('author-guidelines','materials_methods',"""<p>This section must provide sufficient detail to allow the work to be reproduced. Methods already published should be indicated by reference, and only relevant modifications should be described. The sources of all major instruments, chemicals, reagents, assay kits and drugs must be given. The type of statistical tool(s) used to analyse the data should be mentioned and justified. All procedures involving experimental animals or human subjects must be accompanied by a statement on ethical approval.</p>""",9)

s('author-guidelines','discussion',"""<p>This section should relate the Results Section to the current understanding of the scientific problems being investigated in the field. This section must also present the theoretical implications and practical applications of the findings. The authors should also identify where their findings agree and/or contrast with previously published studies. Reasons for such differences must also be advanced.</p>""",10)

s('author-guidelines','conclusion',"""<p>The conclusion must reflect the judgment or decision reached by reasoning after the discussion on the manuscript. This section sums up the arguments about what you have been writing about.</p>""",11)

s('author-guidelines','acknowledgements',"""<p>Major contributors who did not qualify as authors should be acknowledged accordingly. Funding sources should also be acknowledged appropriately.</p>""",12)

s('author-guidelines','submission',"""<p>This should be done <strong>ONLY</strong> online at the journal website. Submission of the manuscript through any other means will not be processed.</p>""",13)

s('author-guidelines','assessment',"""<p>Each manuscript will be subjected to both plagiarism check and preliminary editorial review before it can be sent for double-blind peer review. Manuscripts will only be accepted after satisfactory recommendations have been received from the independent reviewers. Acceptance of manuscripts for publication will be based on originality of the research and contribution to scientific knowledge, without neglecting technical quality.</p>""",14)

s('author-guidelines','publication_fees',"""<p>An article publication fee of Thirty Thousand Naira only (NGN 30,000.00) or One Hundred Dollars (100 USD) will be charged on any article accepted for publication. Payment details will be provided upon acceptance.</p>""",15)

s('author-guidelines','checklist',"""<ul class="list-disc pl-5 space-y-2">
<li>The manuscript has not been previously published nor under consideration by another journal.</li>
<li>The manuscript file is in OpenOffice, Microsoft Word, RTF or WordPerfect document file format.</li>
<li>Where available, URLs and DOIs for the references have been provided.</li>
<li>The text is double-spaced; uses a 12-point font; employs italics, rather than underlining (except with URL addresses).</li>
<li>All illustrations, figures, and tables are placed within the text at the appropriate points rather than at the end.</li>
<li>A declaration statement on conflict of interest.</li>
<li>A cover letter stating the novelty and significance of the work, and a list of at least three suggested reviewers with their email.</li>
</ul>""",16)

# ═══════════════════════════════════════════════════════════
# REVIEWER GUIDELINES — Headings: Confidentiality | Objectivity |
# Conflicts of interest | Timeliness | Scope and quality | Review report
# ═══════════════════════════════════════════════════════════
wipe('reviewer-guidelines','intro','confidentiality','objectivity','conflict_of_interest','timeliness','scope_quality','review_report','benefit_reviewers')

s('reviewer-guidelines','intro',"""<p>Thank you for agreeing to review a manuscript for JHST. Your review will help us maintain our journal's high quality and relevance. Please read the following instructions carefully before you start your review.</p>""",1)

s('reviewer-guidelines','confidentiality',"""<p>The manuscript you are reviewing should not be shared or discussed with anyone outside the review process. You should also not use any information or data from the manuscript for your benefit or advantage. If you have any conflicts of interest with the manuscript or the authors, please inform the editorial office immediately and decline the review invitation.</p>""",2)

s('reviewer-guidelines','objectivity',"""<p>The reviewers should consider the manuscript objectively without any consideration of the authors' race, religion, ethnicity, political affiliation, age, or whatsoever. The assessment by the reviewers should be conducted objectively, supported with data and the arguments should be clearly expressed without personal criticism of any of the authors.</p>""",3)

s('reviewer-guidelines','conflict_of_interest',"""<p>If any of the reviewers have a conflict of interest in any manuscript resulting from a collaboration, competition, or any other connection with any of the authors, companies, or institutions connected to the papers, the reviewer should not consider the manuscript.</p>""",4)

s('reviewer-guidelines','timeliness',"""<p>Please complete your review within four weeks from the invitation date. If you need more time or cannot complete the review, please get in touch with the editorial office as soon as possible and suggest alternative reviewers if possible.</p>""",5)

s('reviewer-guidelines','scope_quality',"""<p>Please evaluate the manuscript according to its scope, originality, significance, quality, and clarity. The manuscript should fit the aims and scope of JHST and contribute substantially to the fields of Hydrocarbon Science and Technology. The manuscript should also be well-written, well-structured, well-referenced, and free of errors and plagiarism.</p>""",6)

s('reviewer-guidelines','review_report',"""<p class="mb-4">Please provide a detailed and constructive review report to help the authors improve their manuscript and the editor decide. Your report should include the following sections:</p>
<ul class="list-none space-y-4 ml-4">
<li><strong class="text-primary block mb-1">Summary:</strong> Provide a summary of the manuscript's main aim, findings, and strengths.</li>
<li><strong class="text-primary block mb-1">General comments:</strong> Provide your overall assessment of the manuscript, highlighting its merits and weaknesses.</li>
<li><strong class="text-primary block mb-1">Specific comments:</strong> Provide specific comments on each section of the manuscript.</li>
<li><strong class="text-primary block mb-1">Recommendation:</strong> Accept | Accept after Minor Revisions | Reconsider after Major Revisions | Reject</li>
</ul>
<p class="mt-4">Reviewers who have reviewed for the journal shall have the benefit of a twenty per cent (20%) waiver when publishing with the journal in our subsequent two editions.</p>""",7)

# ═══════════════════════════════════════════════════════════
# PUBLICATION SCHEDULE — Headings: Biannual Publication | Online First | Special Issues
# ═══════════════════════════════════════════════════════════
wipe('publication-schedule','intro','biannual_publication','online_first','special_issues')

s('publication-schedule','intro',"""<p class="text-lg">The Journal of Hydrocarbon Science and Technology (JHST) adheres to a regular publication schedule to ensure timely dissemination of research.</p>""",1)

s('publication-schedule','biannual_publication',"""<p class="mb-4">JHST publishes two regular issues per calendar year:</p>
<ul class="space-y-4">
<li class="flex items-center bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">
<span class="material-icons text-primary mr-4 text-3xl">calendar_today</span>
<div><span class="block font-bold text-lg text-primary">June</span><span class="text-sm text-gray-600 dark:text-gray-400">Issue 1</span></div>
</li>
<li class="flex items-center bg-gray-50 dark:bg-gray-800 p-4 rounded border border-gray-100 dark:border-gray-700">
<span class="material-icons text-primary mr-4 text-3xl">calendar_today</span>
<div><span class="block font-bold text-lg text-primary">December</span><span class="text-sm text-gray-600 dark:text-gray-400">Issue 2</span></div>
</li>
</ul>""",2)

s('publication-schedule','online_first',"""<p>To minimize publication lag, accepted articles are published individually online as "Articles in Press" immediately after final proofreading, before they are assigned to a specific issue. This ensures your research is available to the community as quickly as possible.</p>""",3)

s('publication-schedule','special_issues',"""<p>The journal occasionally publishes Special Issues focused on emerging topics or conference proceedings. Calls for papers for special issues are announced in the <a class="text-primary hover:underline font-bold" href="/announcements/">Announcements</a> section.</p>""",4)

# ═══════════════════════════════════════════════════════════
# PUBLICATION FEES — Headings: Article Processing Charge (APC) |
#                    Submission Fees | Waiver Policy
# ═══════════════════════════════════════════════════════════
wipe('publication-fees','intro','apc','submission_fees','waiver_policy','payment_methods')

s('publication-fees','intro',"""<p>As an Open Access journal, JHST relies on Article Processing Charges (APCs) to cover the costs of peer review, copyediting, typesetting, long-term archiving, and journal management.</p>""",1)

s('publication-fees','apc',"""<div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-4">
<div class="bg-gray-50 dark:bg-gray-800 p-6 rounded border border-gray-100 dark:border-gray-700 text-center">
<p class="text-sm text-gray-500 font-bold uppercase tracking-wider mb-2">International Authors</p>
<p class="text-4xl font-bold text-primary">$20 <span class="text-lg font-normal text-gray-500">USD</span></p>
</div>
<div class="bg-gray-50 dark:bg-gray-800 p-6 rounded border border-gray-100 dark:border-gray-700 text-center">
<p class="text-sm text-gray-500 font-bold uppercase tracking-wider mb-2">Domestic Authors (Nigeria)</p>
<p class="text-4xl font-bold text-primary">NGN 30,000 <span class="text-lg font-normal text-gray-500">NGN</span></p>
</div>
</div>
<p class="text-sm text-gray-600 dark:text-gray-400 italic">* Fees are subject to change. The applicable fee is the one in effect at the time of submission.</p>""",2)

s('publication-fees','submission_fees',"""<p>There are <strong>NO submission fees</strong>. Authors are only required to pay the APC after their manuscript has been accepted for publication.</p>""",3)

s('publication-fees','waiver_policy',"""<p>JHST offers partial or full fee waivers to authors from low-income countries or those demonstrating genuine financial need. Requests for waivers must be made at the time of submission.</p>
<p class="mt-4">Payment details (Bank Transfer/Online Payment) will be included in the acceptance letter. Please do not make any payments until you receive an official invoice from the Editorial Office.</p>""",4)

# ═══════════════════════════════════════════════════════════
# ETHICS & MALPRACTICE — Headings: Responsibilities of Editors |
# Responsibilities of Reviewers | Responsibilities of Authors | Roles of the Publisher
# ═══════════════════════════════════════════════════════════
wipe('ethics-malpractice','intro','editors_responsibilities','reviewers_responsibilities','authors_responsibilities','publisher_roles')

s('ethics-malpractice','intro',"""<p>The Journal of Hydrocarbon Science and Technology (JHST) is a double-blind peer-reviewed journal. The Journal Publication Committee is committed to ensuring that the editorial process of the journal is governed by rigorous ethical and malpractice standards that are both fair and transparent. We follow the <a class="text-primary hover:underline" href="https://publicationethics.org/files/u2/Best_Practice.pdf" target="_blank">COPE Code of Conduct and Best Practice Guidelines for Journal Editors</a>.</p>""",1)

s('ethics-malpractice','editors_responsibilities',"""<ul class="list-disc pl-5 space-y-2">
<li>The editors are to determine which manuscripts submitted to the journal should be published based on merit only, not on the author's race, citizenship, religion, ethnicity, gender or political beliefs.</li>
<li>The editors are to subject any submitted manuscript to originality test by the use of the appropriate software and send out the blinded copy for the peer-review process.</li>
<li>The editors recommend to the Editor-in-Chief which manuscripts to be accepted or rejected during the review process.</li>
<li>Keeping confidentiality of the authors by ensuring that no information about the author(s) is revealed to the reviewers and vice-versa.</li>
<li>Editors are to ensure the best international ethical practices by ensuring that all accepted manuscripts meet the international best practices.</li>
<li>The editors shall ensure that materials from all unpublished works submitted to the journal are not used in their work.</li>
</ul>""",2)

s('ethics-malpractice','reviewers_responsibilities',"""<ul class="list-disc pl-5 space-y-2">
<li><strong>Confidentiality:</strong> Any information regarding the submitted manuscript should be strictly kept confidential and shouldn't be discussed with a third party without the permission of the editor.</li>
<li><strong>Conflict of interest:</strong> If any of the reviewers have a conflict of interest, the reviewer should not consider the manuscript.</li>
<li><strong>Unbiasedness:</strong> The reviewers should consider the manuscript objectively without any consideration of the authors' race, religion, ethnicity, or political affiliation.</li>
<li><strong>Objectivity:</strong> The assessment by the reviewers should be conducted objectively, supported with data and the arguments clearly expressed without personal criticism.</li>
<li><strong>Celerity:</strong> The review should be conducted promptly as stipulated by the editor.</li>
<li><strong>Acknowledgement of sources:</strong> The reviewers must make sure that the authors have acknowledged and cited all sources of data used in the research.</li>
<li><strong>Plagiarism and other ethical concerns:</strong> The reviewers should notify the editor if they suspect any plagiarism or other unethical practices concerning the manuscript.</li>
</ul>""",3)

s('ethics-malpractice','authors_responsibilities',"""<ul class="list-disc pl-5 space-y-2">
<li><strong>Authorship of the Paper:</strong> Authorship should be limited to all those who have made substantial contributions to the conception, design, execution and analysis/interpretation of data.</li>
<li><strong>Originality:</strong> Authors must ensure that the submitted article is original in content and has not been previously published or is being considered for publication elsewhere.</li>
<li><strong>Human and animal welfare:</strong> It is the duty of the authors to ensure that adequate consideration has been given to the welfare of human and animal subjects used in the work.</li>
<li><strong>Declaration of any conflict of interest:</strong> Authors must declare any conflict of interest that may arise from an article, including the source of funding.</li>
<li><strong>Avoidance of plagiarism:</strong> Authors must ensure that the works of others are properly cited.</li>
</ul>""",4)

s('ethics-malpractice','publisher_roles',"""<ul class="list-disc pl-5 space-y-2">
<li>To provide practical support to the Editor-in-Chief and Editorial Board in following the <a class="text-primary hover:underline" href="https://publicationethics.org/files/Code_of_conduct_for_journal_editors_Mar11.pdf">COPE Code of Conduct for journals</a>.</li>
<li>To ensure the autonomy of editorial decisions.</li>
<li>To protect intellectual property and copyright, and arbitrate in disputes.</li>
<li>To carry out copy-editing, proofreading, type-setting and styling of materials.</li>
<li>To ensure the linking of articles to open and accessible databases.</li>
<li>To arrange and manage scholarly peer review.</li>
<li>To maintain the scholarly record.</li>
<li>To disseminate research data to researchers and other stakeholders.</li>
</ul>""",5)

# ═══════════════════════════════════════════════════════════
# JOURNAL POLICIES — Headings: Open Access Policy | Plagiarism Policy |
#                    Peer Review Policy | Archiving Policy
# ═══════════════════════════════════════════════════════════
wipe('policies','intro','open_access_section','plagiarism_section','peer_review_section','archiving_section')

s('policies','intro',"""<p class="text-lg">JHST is committed to upholding the highest standards of publication ethics and transparency. Please review our key policies below:</p>""",1)

s('policies','open_access_section',"""<p>JHST provides immediate <strong>Open Access</strong> to its content on the principle that making research freely available to the public supports a greater global exchange of knowledge. Users have the right to read, download, copy, distribute, print, search, or link to the full texts of articles.</p>
<p class="mt-4">Authors retain the copyright of their work and grant the journal the right of first publication. Articles are licensed under the <a class="text-primary hover:underline" href="https://creativecommons.org/licenses/by/4.0/" target="_blank">Creative Commons Attribution 4.0 International License (CC BY 4.0)</a>.</p>""",2)

s('policies','plagiarism_section',"""<p>Each manuscript will be subjected to a plagiarism check before being sent for double-blind peer review. Manuscripts will only be processed for peer review if the similarity index is not more than ten (10) percent. This Journal uses Plagiarism CheckerX (or equivalent industry standard software) for its similarity index check.</p>""",3)

s('policies','peer_review_section',"""<p class="mb-4">All submissions to JHST are subject to specific review processes:</p>
<ol class="list-decimal pl-5 space-y-2">
<li><strong>Initial Evaluation:</strong> The Editor-in-Chief determines if the manuscript fits the journal's scope and quality standards.</li>
<li><strong>Double-Blind Peer Review:</strong> At least two independent reviewers evaluate the manuscript without knowing the authors' identities (and vice versa).</li>
<li><strong>Decision:</strong> Based on reviewers' reports, the Editor makes a decision (Accept, Minor Revision, Major Revision, or Reject).</li>
</ol>""",4)

s('policies','archiving_section',"""<p>JHST utilizes digital archiving systems to ensure the long-term preservation of its content. Journal of Hydrocarbon Science and Technology is archived in the Open Journal System (OJS) Public Knowledge Project Preservation Network (PKP PN). Authors are also encouraged to self-archive their accepted manuscripts in institutional or thematic repositories.</p>""",5)

# ═══════════════════════════════════════════════════════════
# PEER REVIEW POLICY — Heading: Guidelines for Double-Blind Peer Review
# ═══════════════════════════════════════════════════════════
wipe('peer-review-policy','intro','double_blind_guidelines')

s('peer-review-policy','intro',"""<p>The Journal of Hydrocarbon Science and Technology (JHST) operates a <strong>Double-Blind Peer Review Policy</strong>. The double-blind peer review procedure guarantees objectivity and avoids prejudice during the review process. When a review is conducted double-blindly, neither the reviewer nor the author knows each other's identity.</p>
<p class="mt-4">The JHST double-blind review process begins with submitting your manuscript. Our editor decides whether your paper is a good fit based on our pre-review assessment, which includes a plagiarism check and conformity with the authors' guidelines.</p>""",1)

s('peer-review-policy','double_blind_guidelines',"""<p class="mb-4">JHST employs double-blind peer review for all its articles. To ensure the success of this process, the author(s) need to ensure that their manuscripts are prepared in a manner that does not reveal their identity. Authors should:</p>
<ul class="list-disc pl-5 space-y-2">
<li>Submit a <strong>Title Page</strong> containing the Author details and a <strong>Blinded Manuscript</strong> with no author details as two (2) separate files.</li>
<li>When referencing prior work, use the third person case. For example, instead of "as we have shown in our previous work," say "has been shown by (Anonymous, 2023)".</li>
<li>Ensure that tables or figures do not contain any pointer to the author's affiliation.</li>
<li>Eliminate all mentions of financing sources and acknowledgements.</li>
<li>Make sure document properties are anonymized.</li>
</ul>""",2)

# ═══════════════════════════════════════════════════════════
# OPEN ACCESS POLICY — No sub-headings on live site
# ═══════════════════════════════════════════════════════════
wipe('open-access-policy','content')

s('open-access-policy','content',"""<p>This journal provides immediate open access to its content on the principle that making research freely available to the public supports a greater global exchange of knowledge. Authors retain copyright of their work, with first publication rights granted to Journal of Hydrocarbon Science and Technology (JHST). Articles in JHST are published on the <a class="text-primary hover:underline" href="https://creativecommons.org/licenses/by/4.0/" target="_blank">Creative Commons Attribution 4.0 International license (CC BY 4.0)</a>.</p>""",1)

print("\nAll sections configured successfully!")
