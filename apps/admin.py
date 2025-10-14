from importlib.resources._common import _

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    def get_form(self, request,obj=None,**kwargs):
        form = super().get_form(request,obj,**kwargs)
        username_field = self.username_field
        if username_field in form.base_fields:
            form.base_fields[username_field].label = "Email / Phone Number"
        return form

    list_display = ("id", "email", "phone", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "phone")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )
