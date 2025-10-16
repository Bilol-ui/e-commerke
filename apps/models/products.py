import os.path
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models import CharField, TextField, ForeignKey, CASCADE, DecimalField, ImageField, PositiveIntegerField, \
    JSONField, BooleanField

from apps.models.base import BaseModel


class Category(BaseModel):
    name = CharField(max_length=100, unique=True)
    description = TextField(blank=True, null=True)


class Product(BaseModel):
    name = CharField(max_length=255)
    category = ForeignKey('apps.Category',CASCADE,related_name='products')
    price = DecimalField(max_digits=10,decimal_places=2)
    description = TextField(blank=True,null=True)
    image = ImageField(upload_to="products/",blank=True,null=True)
    stock = PositiveIntegerField(default=0)
    attributes = JSONField(default=dict,blank=True)

class ProductImage(BaseModel):
    product = ForeignKey('apps.Product',CASCADE,related_name="product-images")
    image = ImageField(upload_to='products/')
    is_main = BooleanField(default=False,help_text='Asosiy rasmmi?')

    def save(self,*args,**kwargs):
        if self.image:
            filename = os.path.splitext(self.image.name)[0]
            img = Image.open(self.image)

            img = img.resize(800,800)

            buffer = BytesIO()
            img.save(buffer,format="WEBP",quality=90)
            webp_image = ContentFile(buffer.getvalue())
            self.image.save(f"{filename}.webp",webp_image,save=False)

        super().save(*args,**kwargs)

