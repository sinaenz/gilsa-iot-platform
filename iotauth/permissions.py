from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    message = {'detail': ' دسترسی'}
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdminUser(BasePermission):
    message = {'detail': 'نیازمند دسترسی ادمین'}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)