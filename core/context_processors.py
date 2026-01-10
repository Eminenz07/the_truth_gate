from dashboard.models import SiteSettings

def site_settings(request):
    """
    Context processor to make site settings available globally in templates.
    """
    return {'site_config': SiteSettings.load()}
