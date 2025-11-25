import os.path
from io import BytesIO

from apps.models.base import CreatedBaseModel
from django.core.files.base import ContentFile
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DecimalField,
    ForeignKey,
    ImageField,
    PositiveIntegerField,
    SlugField,
    TextField,
)
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from PIL import Image


class Category(MPTTModel):
    name = CharField(max_length=255)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='subcategories')
    icon = CharField(blank=True, null=True)
    slug = SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Product(CreatedBaseModel):
    name = CharField(max_length=255)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField(blank=True, null=True)
    slug = SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    image = ImageField(upload_to='products/')
    is_main = BooleanField(default=False, help_text="Asosiy rasm")

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductImages(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name="product_images")
    image = ImageField(upload_to='products/')
    is_main = BooleanField(default=False, help_text='Asosiy rasmmi?')

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
