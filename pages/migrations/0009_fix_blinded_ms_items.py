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


def fix_blinded_ms_items(apps, schema_editor):
    PeerReviewPolicyPage = apps.get_model('pages', 'PeerReviewPolicyPage')
    try:
        page = PeerReviewPolicyPage.objects.get(pk=1)
    except PeerReviewPolicyPage.DoesNotExist:
        return

    # Force-update: existing content is a flat <p> with no list structure
    if '<ul>' not in (page.blinded_ms_items or ''):
        page.blinded_ms_items = BLINDED_MS_ITEMS
        page.save()


def reverse_fix(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_populate_peer_review_page'),
    ]

    operations = [
        migrations.RunPython(fix_blinded_ms_items, reverse_fix),
    ]
