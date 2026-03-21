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
