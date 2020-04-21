from rest_framework import permissions
from django.contrib.auth import authenticate, login as dj_login
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.authtoken.models import Token

# Custom Authentication class to only grant access if Token is valid and CSRF has been provided


class CustomAuth(permissions.BasePermission):
    """
    Custom permission to only allow users with Token and CSRF token access
    """

    def has_permission(self, request, view):
        # check csrf
        request.csrf_processing_done = False
        reason = CsrfViewMiddleware().process_view(request, None, (), {})
        if reason is not None:
            return False

        # Check token exists in headers
        if 'token' in request.COOKIES:
            token_value = request.COOKIES['token']

            # Check if token value exists
            if Token.objects.filter(key=token_value).exists():

                # Maybe do some additional blacklist filtering?
                return True

        # If none provided, permission denied
        return False
