from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return user.is_authenticated and user.role in ['admin','moderator']


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            return request.user.role in ["admin","moderator"]
        return False