from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedStaffWriteOtherwiseReadOnly(BasePermission):
    """
    Require authentication for all requests. Allow SAFE_METHODS to any
    authenticated user; require staff for writes.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_staff or user.is_superuser
