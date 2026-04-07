from .models import Page

def sidebar_context(request):
    """
    Makes the CMS sidebar page and its sections available sitewide.
    """
    try:
        index_page = Page.objects.get(slug='index')
        sidebar_sections = index_page.sections.filter(section_key__startswith='sidebar_').order_by('order')
        return {'sidebar_sections': sidebar_sections}
    except Page.DoesNotExist:
        return {'sidebar_sections': None}
