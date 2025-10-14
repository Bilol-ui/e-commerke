import os.path

from PIL import Image
from django.db.models import TextField, DecimalField, ImageField, ForeignKey, CASCADE
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField

from apps.models.base import BaseModel


class Product(BaseModel):
    class CategoryEnum(TextChoices):
        KEYBOARD = "keyboard","Keyboard"
        MONITOR = "monitor","Monitor"
        PHONE = "phone","Phone"
        PS5 = "ps5","PlayStation 5"
        OTHER = "other","Otger"

    class ColorEnum(TextChoices):
        Black = "black","Black"
        WHITE = "white","White"
        RED = "red","Red"
        BLUE = "blue","Blue"
        GREEN = "green","Green"
        GRAY = "gray","Gray"
        NONE = "none", "No Color"


    class SizeEnum(TextChoices):
        SMALL = "small","Small"
        MEDIUM = "medium","Medium"
        LARGE = "large", "Large"
        XLARGE = "xlarge","Extra Large"
        NONE = "none","No SIZE"

    name = CharField(max_length=255)
    category = CharField(
        max_length=50, choices=CategoryEnum.choices,default=CategoryEnum.OTHER
    )
    description = TextField(blank=True)
    price = DecimalField(max_digits=10,decimal_places=2)

    color = CharField(
        max_length=20,choices=ColorEnum.choices,default=ColorEnum.NONE, blank=True
    )

    size = CharField(
        max_length=20, choices=SizeEnum.choices,default=SizeEnum.NONE,blank=True
    )

    ram = CharField(max_length=50,blank=True,null=True)
    cpu = CharField(max_length=50,blank=True,null=True)

    image = ImageField(upload_to="products/")

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)
            img = img.resize(600,600)

            web_path = os.path.splitext(img_path)[0] + ".webp"
            img.save(web_path,"WEBP",quality=90)

            self.image.name = "products/" + os.path.basename(web_path)
            super().save(update_fields=["image"])

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class ProductsImage(BaseModel):
    product = ForeignKey(
        Product,CASCADE,related_name="images"
    )
    image = ImageField(upload_to="products/")

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)
            img = img.resize(600,600)

            webp_path = os.path.splitext(img_path)[0] + ".webp"
            img.save(webp_path,"WEBP",quality=90)

            self.image.name = "products/" + os.path.basename(webp_path)
            super().save(update_fields=['image'])

    def __str__(self):
        return f"{self.product.name} - Image"
