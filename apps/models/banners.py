from django.db.models import CharField, ImageField, BooleanField

from apps.models.base import CreatedBaseModel


class Banner(CreatedBaseModel):
    title = CharField(max_length=255)
    image = ImageField(upload_to='banners/')
    is_active = BooleanField(default=True)