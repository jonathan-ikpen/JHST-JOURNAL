from django.db import migrations


def text_to_ul(text):
    """Convert newline-delimited plain text into <ul><li> HTML."""
    items = [line.strip() for line in text.split('\n') if line.strip()]
    if not items:
        return ''
    lis = ''.join(f'<li>{item}</li>' for item in items)
    return f'<ul>{lis}</ul>'


def wrap_p(text):
    """Wrap plain text in <p> if it has no block-level HTML tags."""
    t = text.strip()
    if not t:
        return t
    if t.startswith('<'):
        return t
    return f'<p>{t}</p>'


def fix_aim_scope(apps, schema_editor):
    AimScopePage = apps.get_model('pages', 'AimScopePage')
    try:
        page = AimScopePage.objects.get(pk=1)
    except AimScopePage.DoesNotExist:
        return

    changed = False

    # Convert newline-delimited scope columns to <ul><li> lists
    for field in ('scope_col1', 'scope_col2'):
        val = getattr(page, field) or ''
        if val and '<ul>' not in val:
            setattr(page, field, text_to_ul(val))
            changed = True

    # Wrap plain-text paragraphs in <p> tags
    for field in ('aim_text', 'scope_intro', 'intro_text'):
        val = getattr(page, field) or ''
        if val and not val.strip().startswith('<'):
            setattr(page, field, wrap_p(val))
            changed = True

    if changed:
        page.save()


def reverse_fix(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_fix_blinded_ms_items'),
    ]

    operations = [
        migrations.RunPython(fix_aim_scope, reverse_fix),
    ]
