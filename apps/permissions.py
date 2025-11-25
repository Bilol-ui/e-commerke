from rest_framework.permissions import BasePermission, SAFE_METHODS


class RoleBasedPermission(BasePermission):
    """
    Auth bo‘lgan user:
      - GET → hamma
      - POST/PUT/PATCH/DELETE → faqat admin/moderator
    """

    def has_permission(self, request, view):
        # Auth bo‘lmagan user → ruxsat yo‘q
        if not request.user.is_authenticated:
            return False

        # Safe method → barcha
        if request.method in SAFE_METHODS:
            return True

        # CRUD → admin/moderator
        return request.user.role in ["admin", "moderator"]
