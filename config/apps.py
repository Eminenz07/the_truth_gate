from django.contrib.admin.apps import AdminConfig

class MinistryAdminConfig(AdminConfig):
    default_site = 'config.admin.MinistryAdminSite'
