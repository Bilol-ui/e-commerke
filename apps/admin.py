from apps.models import Category, Product, ProductImage, User
from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from mptt.admin import MPTTModelAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Admin ro‘yxatda chiqadigan ustunlar
    list_display = ("id", "email", "phone", "role", "is_active", "is_staff")
    list_display_links = ("id", "email")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "phone")
    ordering = ("-id",)

    # Admin formda ko‘rsatiladigan maydonlar
    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Role", {"fields": ("role",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone", "password1", "password2", "role", "is_staff", "is_active"),
        }),
    )

    # # ✅ Login formasida Email / Phone label chiqishi uchun
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     username_field = self.username_field
    #     if username_field in form.base_fields:
    #         form.base_fields[username_field].label = "Email / Phone number"
    #     return form


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("id", "name", "parent", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("parent",)
    ordering = ("name",)
    mptt_level_indent = 20
    list_display_links = ("id", "name")


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "is_main")
    readonly_fields = ()




@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("id", "name", "category", "price", "slug")
    search_fields = ("name", "description")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-id",)
    inlines = [ProductImageInline]
    list_display_links = ("id", "name")
    save_on_top = True


@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    list_display = ("id", "product", "is_main")
    list_filter = ("is_main", "product")
    search_fields = ("product__name",)
    ordering = ("-id",)



