import re

from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField

from apps.models import Product, ProductImage
from apps.models.banners import Banner
from apps.models.carts import CartItem, Cart, Wishlist, OrderItem, Order, OrderHistory
from apps.models.products import Category, ProductVariant
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        phone = attrs.get("phone")

        # ❗ Faqat bittasini kiritish kerak
        if (not email and not phone) or (email and phone):
            raise ValidationError("Faqat bittasini kiriting: email yoki telefon raqami.")

        # ✅ Email bo‘lsa tekshiruv
        if email:
            if not email.endswith("@gmail.com"):
                raise ValidationError("Email faqat @gmail.com bilan tugashi kerak.")
            if User.objects.filter(email=email).exists():
                raise ValidationError("Bu email allaqachon ro‘yxatdan o‘tgan.")

        # ✅ Telefon bo‘lsa tekshiruv
        if phone:
            if not phone.startswith("+998"):
                raise ValidationError("Telefon raqam +998 bilan boshlanishi kerak.")
            clean_phone = re.sub(r"\D", "", phone)
            if len(clean_phone) != 12:
                raise ValidationError("Telefon raqam uzunligi 12 ta raqam bo‘lishi kerak.")
            if User.objects.filter(phone=phone).exists():
                raise ValidationError("Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.")

        return attrs


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductModelSerializer(ModelSerializer):
    category = CategoryModelSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductVariantModelSerializer(ModelSerializer):
    # product nomini o‘qish uchun (faqat ko‘rinish, o‘zgartirib bo‘lmaydi)
    product_name = CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "product_name",
            "color",
            "size",
            "ram",
            "storage",
            "diagonal",
            "material",
            "price",
            "stock",
            "is_available",
        ]
        read_only_fields = ["is_available"]


class BannerModelSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'is_active', 'created_at', 'updated_at']

class CartItemModelSerializer(ModelSerializer):
    product_name = CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price']


class CartModelSerializer(ModelSerializer):
    items = CartItemModelSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total', 'items']

class WishListModelSerializer(ModelSerializer):
    product_names = SlugRelatedField(many=True,read_only=True,slug_field='name',source='products')

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product_names']

class OrderItemModelSerializer(ModelSerializer):
    product_name = CharField(source='product.name',read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price']

class OrderModelSerializer(ModelSerializer):
    items = OrderItemModelSerializer(many=True,read_only=True)
    item_count = IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'status', 'item_count', 'items', 'created_at']


class OrderHistorySerializer(ModelSerializer):
    user_name = CharField(source='user.username', read_only=True)

    class Meta:
        model = OrderHistory
        fields = ['id', 'order', 'user', 'user_name', 'action', 'description', 'created_at']

