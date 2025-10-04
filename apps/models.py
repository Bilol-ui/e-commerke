from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, CharField, BooleanField, Model, OneToOneField, CASCADE, DateTimeField, \
    IntegerField
from django.utils.timezone import now


class User(AbstractUser):
    username = None
    email = EmailField(unique=True, null=True, blank=True)
    phone =  CharField(max_length=20, unique=True, null=True, blank=True)
    is_verified = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or self.phone


class PhoneVerification(Model):
    user = OneToOneField(User, CASCADE)
    code = CharField(max_length=6)
    created_at = DateTimeField(auto_now_add=True)
    attempts = IntegerField(default=0)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=1)