from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = 'permission denied, you are not the admin'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)
