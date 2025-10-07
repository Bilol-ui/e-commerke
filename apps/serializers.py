import os.path
import re

from PIL import Image
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import User, ProductImage, Product


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone", "password"]

    def validate_email(self, value):
        if not value:
            ValidationError("You must write your email")

        email_ = User.objects.filter(email=value).exists()
        if not value.endswith('@gmail.com'):
            ValidationError('email must ends with @gmail.com')

        if email_:
            ValidationError('this email already exists')

        return value

    def validate_phone(self, value):
        if not value.isdigit():
            ValidationError('phone number must be digits +998991234567')

        if not value.startswith('+998'):
            ValidationError('Phone number must started with +998')

        clean_phone = re.sub(r"\D", "", value)

        if len(clean_phone) != 12:
            ValidationError('phone numbers length must be 12 digits')

        return clean_phone

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image']

    def create(self,validated_data):
        instance = super().create(validated_data)

        if instance.image:
            img_path = instance.image.path
            img = Image.open(img_path)

            img = img.resize(600,600)
            webp_path = os.path.splitext(img_path([0]))
            img.save(webp_path,"WEBP")

            instance.image.name = "products/" + os.path.basename(webp_path)
            instance.save(update_fields=["image"])
        return instance

class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "size", "color", "images"]
