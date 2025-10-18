from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, CharField, BooleanField


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError("Email yoki phone number kiritilishi zarur")

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuserda is_staff=Tru boishi kerak")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuserda is-superuser=True bolishi kerak")

        return self.create_user(email=email, phone=phone, password=password, **extra_fields)


class User(AbstractUser):
    username = None
    email = EmailField(unique=True, null=True, blank=True)
    phone = CharField(max_length=20, unique=True, null=True, blank=True)
    is_verified = BooleanField(db_default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.phone
