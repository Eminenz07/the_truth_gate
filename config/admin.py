from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class MinistryAdminSite(AdminSite):
    site_header = _("The Truth Gate Ministry Portal")
    site_title = _("Ministry Admin")
    index_title = _("Dashboard")
    
    def get_app_list(self, request, *args, **kwargs):
        """
        Reorder the apps to put Ministry features first.
        """
        app_list = super().get_app_list(request, *args, **kwargs)
        
        # Define preferred order
        ordering = {
            'Sermons': 1,
            'Events': 2,
            'Ministry': 3,
            'Core': 4,
            'Authentication and Authorization': 99
        }
        
        app_list.sort(key=lambda x: ordering.get(x['name'], 50))
        return app_list
