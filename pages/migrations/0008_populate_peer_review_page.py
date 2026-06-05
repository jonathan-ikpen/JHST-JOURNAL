from django.db import migrations


BLINDED_MS_ITEMS = (
    '<ul>'
    '<li>When referencing the Authors’ prior work, use the third person case. '
    'For example, instead of saying “as we have shown in our previous work,” '
    'say “has shown by (Anonymous, 2023)”.</li>'
    '<li>Ensure that tables or figures do not contain any pointer to the author’s affiliation.</li>'
    '<li>Eliminate all mentions of financing sources.</li>'
    '<li>Leave out the acknowledgements.</li>'
    '<li>Make sure document properties are anonymized and remove any identifiable information '
    'from file names, such as author names.</li>'
    '<li>Refrain from removing necessary self-references or other references, and restrict '
    'self-references to sources that will interest the reviewer of the submitted work.</li>'
    '</ul>'
)

TITLE_PAGE_TEXT = (
    '<p>The title page should contain the title, authors’ names and affiliations, '
    'and a complete address for the corresponding author, including telephone and e-mail addresses.</p>'
)

INTRO_TEXT = (
    '<p>The Journal of Hydrocarbon Science and Technology (JHST) implements a '
    '<strong>Double-Blind Peer Review Policy</strong>, in which neither the reviewer nor '
    'the author knows each other’s identity. This approach enhances objectivity and '
    'prevents bias in the evaluation process.</p>'
)

PROCESS_TEXT = (
    '<p>All submitted manuscripts are first reviewed by the editors for plagiarism and '
    'compliance with journal guidelines. Manuscripts that pass editorial assessment are '
    'sent to at least two reviewers by the editor, with author identities concealed. '
    'Following reviewer feedback, authors revise their manuscript accordingly, and the '
    'review cycle continues until both reviewers approve publication.</p>'
)

DESK_REJECTION_TEXT = (
    '<p>Initial desk rejection occurs within the first week after submission if the article '
    'is not aligned with the journal’s interests or objectives, or if a very preliminary '
    'version has been submitted.</p>'
)

GUIDELINES_INTRO = (
    '<p>Authors are required to submit two separate files: a <strong>title page</strong> '
    'and an <strong>anonymized manuscript</strong>.</p>'
)

BLINDED_MS_INTRO = (
    '<p>When preparing the blinded manuscript, authors should adhere to the following guidelines:</p>'
)


def populate_peer_review_page(apps, schema_editor):
    PeerReviewPolicyPage = apps.get_model('pages', 'PeerReviewPolicyPage')

    try:
        page = PeerReviewPolicyPage.objects.get(pk=1)
    except PeerReviewPolicyPage.DoesNotExist:
        page = PeerReviewPolicyPage(pk=1)

    changed = False

    def fill(field, value):
        nonlocal changed
        if not getattr(page, field):
            setattr(page, field, value)
            changed = True

    fill('intro_text', INTRO_TEXT)
    fill('process_text', PROCESS_TEXT)
    fill('desk_rejection_text', DESK_REJECTION_TEXT)
    fill('guidelines_intro', GUIDELINES_INTRO)
    fill('title_page_text', TITLE_PAGE_TEXT)
    fill('blinded_ms_intro', BLINDED_MS_INTRO)
    fill('blinded_ms_items', BLINDED_MS_ITEMS)

    if changed:
        page.save()


def reverse_populate(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_add_heading_fields'),
    ]

    operations = [
        migrations.RunPython(populate_peer_review_page, reverse_populate),
    ]
