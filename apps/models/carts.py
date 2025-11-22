from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db.models import CASCADE, ForeignKey, PROTECT, CharField, TextChoices, SET_NULL
from django.db.models.fields import PositiveIntegerField, TextField, IntegerField, BigIntegerField
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import DecimalField

from apps.models.base import CreatedBaseModel


class Cart(CreatedBaseModel):
    customer = ForeignKey('apps.User', CASCADE, related_name='cart')

    # total = DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    # @property
    # def total(self):
    #     return sum(item.total for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.customer.phone}"


class CartItem(CreatedBaseModel):
    cart = ForeignKey('apps.Cart', CASCADE, related_name='items')
    product_version = ForeignKey('apps.ProductVariant', CASCADE)
    quantity = IntegerField(_('Quantity'), default=1)
    price = BigIntegerField(_('Price at addition'), default=0)

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product_version.product.name}({self.quantity}x)"


class Wishlist(CreatedBaseModel):
    user = ForeignKey('apps.User', CASCADE, related_name='wishlists')
    product = ForeignKey('apps.Product', CASCADE, related_name='wishlists')

    def __str__(self):
        return f"Wishlist({self.user})"


class Order(CreatedBaseModel):
    class OrderStatus(TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    total = DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def __str__(self):
        return f"Order #{self.id} - {self.user} - {self.status}"

    @property
    def item_count(self):
        return self.items.count()


class OrderItem(CreatedBaseModel):
    order = ForeignKey('apps.Order', CASCADE, related_name='items')
    product = ForeignKey('apps.Product', PROTECT)
    quantity = PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    price = DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class OrderHistory(CreatedBaseModel):
    class ActionType(TextChoices):
        CREATED = "created", "Buyurtma yaratildi"
        STATUS_CHANGED = "status_changed", "Holat o‘zgardi"
        PAYMENT_CONFIRMED = "payment_confirmed", "To‘lov tasdiqlandi"
        ITEM_ADDED = "item_added", "Mahsulot qo‘shildi"
        ITEM_REMOVED = "item_removed", "Mahsulot o‘chirildi"
        CANCELLED = "cancelled", "Buyurtma bekor qilindi"

    order = ForeignKey('Order', CASCADE, related_name='history_records', verbose_name="Buyurtma")
    user = ForeignKey('apps.User', SET_NULL, null=True, blank=True, related_name='order_history_actions',
                      verbose_name="Foydalanuvchi")
    action = CharField(max_length=50, choices=ActionType.choices, default=ActionType.CREATED,
                       verbose_name="Harakat turi")
    description = TextField(blank=True, null=True, verbose_name="Qo‘shimcha ma’lumot (izoh)"
                            )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Buyurtma tarixi"
        verbose_name_plural = "Buyurtmalar tarixi"
