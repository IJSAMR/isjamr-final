from rest_framework import permissions
# from rest_framework import permissions

class IsAdminOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_staff  # Only allow GET if the user is an admin
        return True  # Allow POST requests for all users


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
