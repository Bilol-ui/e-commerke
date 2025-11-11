from apps.models import Product
from django_filters import CharFilter, FilterSet, NumberFilter


class ProductFilter(FilterSet):
    category = CharFilter(field_name="category_name", lookup_expre="icontains")
    color = CharFilter(field_name="color", lookup_expre="icontains")
    size = CharFilter(field_name="size", lookup_expre="icontains")
    price_min = NumberFilter(field_name="size", lookup_expre="icontains")
    price_max = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["category", "color", "size", "price_min", "price_max"]
