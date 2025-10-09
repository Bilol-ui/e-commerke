import os

from PIL import Image
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, CharField, BooleanField, Model, CASCADE, DateTimeField, \
    ForeignKey, ImageField
from django.db.models.enums import TextChoices
from django.db.models.fields import TextField, DecimalField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = EmailField(unique=True)
    phone = CharField(max_length=20, unique=True, null=True, blank=True)
    is_verified = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.phone





class Product(Model):
    class ColorEnum(TextChoices):
        BLACK = "black", "Black"
        WHITE = "white", "White"
        RED = "red", "Red"
        BLUE = "blue", "Blue"
        GREEN = "green", "Green"

    class SizeEnum(TextChoices):
        SMALL = "small", "Small"
        MEDIUM = "medium", "Medium"
        LARGE = "large", "Large"
        XLARGE = "xlarge", "Extra Large"
        NONE = "none", "No Size"

    name = CharField(max_length=255)
    description = TextField(blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)

    # Qo‘shimcha atributlar (hammasi optional)
    size = CharField(
        max_length=20,
        choices=SizeEnum.choices,
        default=SizeEnum.NONE,
    )
    color = CharField(
        max_length=20,
        choices=ColorEnum.choices,
        default=ColorEnum.NONE,
    )
    ram = CharField(max_length=50, blank=True, null=True)
    cpu = CharField(max_length=50, blank=True, null=True)

    # Rasm
    image = ImageField(upload_to="products/")

    created_at = DateTimeField(auto_now_add=True)



class ProductImage(Model):

    product = ForeignKey(Product, CASCADE, related_name='images')
    image = ImageField(upload_to='products/')

    product = ForeignKey(Product, on_delete=CASCADE, related_name="images")
    image = ImageField(upload_to="products/")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            img = img.resize((500, 500))

            webp_path = os.path.splitext(img_path)[0] + ".webp"
            img.save(webp_path, "WEBP")

            self.image.name = "products/" + os.path.basename(webp_path)
            super().save(update_fields=["image"])


    def __str__(self):
        return f"{self.product.name} - Image"

# TODO product keyboard(color), monitor(rang), samsung a56(CPU, RAM, color), jacket(size, color), PS5(color, RAM, CPU)
# TODO redis {'phone': 'code'}  {'email': 'code'}
