from rest_framework import permissions


class HasAPIKeyPermission(permissions.BasePermission):
    """
    The HasAPIKeyPermission class determines if the user request should be processed by verifying if there is a
    valid Bearer token in the header.
    """
    def has_permission(self, request, view):
        """
        Inspect the header and check against for validity.

        :param request:  The API request
        :param view:  The view requesting permission
        :return: True if the API key is valid
        """
        # The API_KEY needs to be in Kubernetes secrets file, but it's fine right here for now
        api_key = request.META.get('HTTP_AUTHORIZATION').split('Bearer ')[1] if request.META.get('HTTP_AUTHORIZATION') else ''
        return api_key == 'MAGIC_KEY'
