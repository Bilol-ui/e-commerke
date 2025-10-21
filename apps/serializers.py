import os
import re
from PIL import Image
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from apps.models import ProductImage, Product
from apps.models.products import Category

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


from rest_framework import serializers
from apps.models import ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    ProductVariant modelini API orqali ko‘rish va yaratish uchun serializer.
    Har bir variant — mahsulotning rang, o‘lcham, RAM, va boshqa xususiyatlarini o‘z ichiga oladi.
    """

    # product nomini o‘qish uchun (faqat ko‘rinish, o‘zgartirib bo‘lmaydi)
    product_name = serializers.CharField(source='product.name', read_only=True)

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
