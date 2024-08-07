from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedUser(IsAuthenticated):
    message = 'You must be authenticated to access this resource.'

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        custom_condition = request.user.is_verified and request.user.password != ''

        return is_authenticated and custom_condition


class IsAuthenticatedToSetPassword(IsAuthenticated):
    message = 'You must be authenticated to access this resource.'

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        custom_condition = request.user.is_verified and request.user.password == ''

        return is_authenticated and custom_condition


class IsAdmin(BasePermission):
    message = 'permission denied, you are not the admin'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)
