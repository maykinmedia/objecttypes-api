from rest_framework.permissions import BasePermission


class IsTokenAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.auth)
