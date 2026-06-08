from .models import SiteSettings

def site_settings_processor(request):
    settings = SiteSettings.objects.first()
    return {
        'site_settings': settings
    }
