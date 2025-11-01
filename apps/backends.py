from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            return None

        user = User.objects.filter(email=username).first() or User.objects.filter(phone=username).first()

        if user and user.check_password(password):
            return user
        return None
