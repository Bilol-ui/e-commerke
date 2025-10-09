import os.path
import re

from PIL import Image
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import User, ProductImage, Product


User = get_user_model()

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email","phone","password"]

    def validate(self, attrs):
        email = attrs.get("email")
        phone = attrs.get("phone")

        if (not email and not phone) or (email and phone):
            raise ValidationError(
                "Faqat bittasini kiriting: email yoki telefon raqami."
            )

            # ✅ Agar email bo‘lsa — tekshiruv
        if email:
            if not email.endswith("@gmail.com"):
                raise ValidationError("Email faqat @gmail.com bilan tugashi kerak.")
            if User.objects.filter(email=email).exists():
                raise ValidationError("Bu email allaqachon ro‘yxatdan o‘tgan.")

<<<<<<< HEAD

=======
        if phone:
            if not phone.startswith("+998"):
                raise ValidationError("phone number +998 bilan boshlanshi kerak")
            clean_phone = re.sub(r"\D", "", phone)
            if len(clean_phone) !=12:
                raise ValidationError("Telefon raqam uzunligi 12 ta raqam bo‘lishi kerak.")
            if User.objects.filter(phone=phone).exists():
                raise ValidationError("Bu phone allaqachon ro‘yxatdan o‘tgan.")
>>>>>>> c382de8 (new add)
class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

<<<<<<< HEAD
    def create(self, validated_data):
        instance = super().create(validated_data)

        if instance.image:
            img_path = instance.image.path
            img = Image.open(img_path)

            img = img.resize(600, 600)
            webp_path = os.path.splitext(img_path([0]))
            img.save(webp_path, "WEBP")

            instance.image.name = "products/" + os.path.basename(webp_path)
            instance.save(update_fields=["image"])
        return instance
=======

>>>>>>> c382de8 (new add)


class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "size", "color", "images"]
