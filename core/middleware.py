from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseForbidden

class DeviceRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access if DEBUG is True (Local Development)
        if settings.DEBUG:
            return self.get_response(request)

        # Protected paths
        protected_paths = ['/admin/', '/dashboard/']
        
        # Check if current path matches any protected path
        is_protected = any(request.path.startswith(path) for path in protected_paths)
        
        if is_protected:
            # Check for trusted cookie
            trust_cookie = request.COOKIES.get(settings.TRUSTED_COOKIE_NAME)
            
            # If no cookie, return 404 to hide the page existence
            if not trust_cookie:
                # We return a 404 (Not Found) instead of 403 (Forbidden) 
                # to obscure the existence of the admin panel.
                from django.http import Http404
                raise Http404()

        response = self.get_response(request)
        return response
