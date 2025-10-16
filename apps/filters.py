from rest_framework.fields import CharField
from django_filters import rest_framework as filters, FilterSet, NumberFilter

from apps.models import Product


class ProductFilter(FilterSet):
    category = CharField(field_name="category_name",lookup_expre="icontains")
    color = CharField(field_name="color",lookup_expre="icontains")
    size = CharField(field_name="size",lookup_expre="icontains")
    price_min = NumberFilter(field_name="size",lookup_expre="icontains")
    price_max = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["category", "color", "size", "price_min", "price_max"]