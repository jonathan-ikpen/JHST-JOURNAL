from .models import Notification

def notifications(request):
    """
    Makes notifications available in all templates when user is authenticated.
    """
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).order_by('-created_at')[:5]
        return {'notifications': unread_notifications}
    return {'notifications': []}

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
