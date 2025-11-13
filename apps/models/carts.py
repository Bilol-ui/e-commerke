from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db.models import OneToOneField, CASCADE, ForeignKey, PROTECT, ManyToManyField, Model, CharField, \
    DateTimeField, TextChoices, SET_NULL
from django.db.models.fields import PositiveIntegerField, TextField
from rest_framework.fields import DecimalField

from apps.models.base import CreatedBaseModel
from root.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


class Cart(CreatedBaseModel):
    user = OneToOneField(User, CASCADE, related_name='cart')
    total = DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def recalc_total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.line_total
        self.total = total
        self.save(update_fields=['total', 'updated_at'])
        return self.total


class CartItem(CreatedBaseModel):
    cart = ForeignKey(Cart, CASCADE, related_name='items')
    product = ForeignKey('products.Product', PROTECT)
    quantity = PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    unit_price = DecimalField(max_digits=12, decimal_places=2)
    line_total = DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        self.line_total = (self.unit_price or self.product.price) * self.quantity
        super().save(*args, **kwargs)
        try:
            self.cart.recalc_total()
        except Exception:
            pass


class Wishlist(CreatedBaseModel):
    user = OneToOneField(User, CASCADE, related_name='wishlist')
    products = ManyToManyField('products.Product', related_name='wishlists', blank=True)

    def __str__(self):
        return f"Wishlist({self.user})"





class Order(CreatedBaseModel):
    class OrderStatus(TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    user = ForeignKey(User, CASCADE, related_name='orders')
    total = DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

    @property
    def item_count(self):
        return self.items.count()


class OrderItem(CreatedBaseModel):
    order = ForeignKey(Order, CASCADE, related_name='items')
    product = ForeignKey('products.Product',PROTECT)
    quantity = PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    unit_price = DecimalField(max_digits=12, decimal_places=2)
    line_total = DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class OrderHistory(CreatedBaseModel):
    class ActionType(TextChoices):
        CREATED = "created","Buyurtma yaratildi"
        STATUS_CHANGED = "status_changed", "Holat o‘zgardi"
        PAYMENT_CONFIRMED = "payment_confirmed", "To‘lov tasdiqlandi"
        ITEM_ADDED = "item_added", "Mahsulot qo‘shildi"
        ITEM_REMOVED = "item_removed", "Mahsulot o‘chirildi"
        CANCELLED = "cancelled", "Buyurtma bekor qilindi"

    order = ForeignKey('Order', CASCADE, related_name='history_records', verbose_name="Buyurtma")
    user = ForeignKey('users.User',SET_NULL,null=True,blank=True,related_name='order_history_actions',verbose_name="Foydalanuvchi")
    action = CharField(max_length=50,choices=ActionType.choices,default=ActionType.CREATED,verbose_name="Harakat turi")
    description = TextField(blank=True,null=True,verbose_name="Qo‘shimcha ma’lumot (izoh)"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Buyurtma tarixi"
        verbose_name_plural = "Buyurtmalar tarixi"

