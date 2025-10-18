import os.path
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models import CharField, TextField, ForeignKey, CASCADE, DecimalField, ImageField, PositiveIntegerField, \
    JSONField, BooleanField, SET_NULL
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.models.base import CreatedBaseModel


class Category(MPTTModel):
    name = CharField(max_length=255, unique=True)
    # TODO icon
    parent = TreeForeignKey('self', SET_NULL, null=True, blank=True, related_name='subcategories')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Product(CreatedBaseModel):
    name = CharField(max_length=255)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    description = TextField(blank=True, null=True)  # TODO ckeditor5
    # price = DecimalField(max_digits=10, decimal_places=2)
    # quantity = PositiveIntegerField(default=0)
    # attributes = JSONField(default=dict, blank=True)


"""
50-talik isitgich (0)
30-talik isitgich (0)
100-talik isitgich (17)

"""


class ProductImage(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name="images")
    image = ImageField(upload_to='products/')
    is_main = BooleanField(db_default=False, help_text='Asosiy rasmmi?')

    def save(self, *args, **kwargs):
        if self.image:
            filename = os.path.splitext(self.image.name)[0]
            img = Image.open(self.image)

            img = img.resize(800, 800)

            buffer = BytesIO()
            img.save(buffer, format="WEBP", quality=90)
            webp_image = ContentFile(buffer.getvalue())
            self.image.save(f"{filename}.webp", webp_image, save=False)

        super().save(*args, **kwargs)
