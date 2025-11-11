from apps.models.base import CreatedBaseModel
from django.db.models import BooleanField, CharField, ImageField


class Banner(CreatedBaseModel):
    title = CharField(max_length=255)
    image = ImageField(upload_to='banners/')
    is_active = BooleanField(default=True)
