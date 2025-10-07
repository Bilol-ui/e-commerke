from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import EmailField, CharField, BooleanField, Model, OneToOneField, CASCADE, DateTimeField, \
    IntegerField, ForeignKey, ImageField
from django.db.models.enums import TextChoices
from django.db.models.fields import TextField, DecimalField
from django.utils.timezone import now


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





class SizeEnum(TextChoices):
    XS = "XS", "EXTRA SMALL"
    S = "s", "SMALL"
    M = "M", "Medium"
    L = "L", "Large"
    XL = "XL", "Extra Large"


class ColorEnum(TextChoices):
    Black = "black", "Black"
    WHITE = "white", "White"
    RED = "red", "Red"
    BLUE = "blue", 'Blue'
    GREEN = "green", "Green"


class Product(Model):
    name = CharField(max_length=200)
    description = TextField(blank=True)
    price = DecimalField(max_digits=10,decimal_places=2)
    size = CharField(max_length=5,choices=SizeEnum, default=SizeEnum.M)
    color = CharField(max_length=5,choices=ColorEnum,default=ColorEnum.Black)

    def __str__(self):
        return self.name

class ProductImage(Model):
    product = ForeignKey(Product,CASCADE,related_name='images')
    image = ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.name} - Image"
