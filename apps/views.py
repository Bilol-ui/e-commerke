from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.models import Category, Product, ProductVariant, ProductImages
from apps.serializers import (
    CategoryModelSerializer,
    ProductModelSerializer,
    ProductVariantModelSerializer,
    ProductImageModelSerializer,
)

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    lookup_field = "slug"

class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().select_related("category")
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "name"]

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().select_related("category")
    serializer_class = ProductModelSerializer
    lookup_field = "slug"

class ProductVariantListCreateAPIView(ListCreateAPIView):
    queryset = ProductVariant.objects.all().select_related("product")
    serializer_class = ProductVariantModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product__slug", "color", "size", "ram", "storage", "is_available"]
    search_fields = ["product__name"]

class ProductVariantDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.all().select_related("product")
    serializer_class = ProductVariantModelSerializer

class ProductImagesListCreateAPIView(ListCreateAPIView):
    queryset = ProductImages.objects.all().select_related("product")
    serializer_class = ProductImageModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product__slug", "is_main"]
    search_fields = ["product__name"]

class ProductImagesDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductImages.objects.all().select_related("product")
    serializer_class = ProductImageModelSerializer
