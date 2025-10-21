from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

from apps.filters import ProductFilter
from apps.models import User, ProductImage, Product
from apps.models.products import Category
from apps.serializers import RegisterSerializer, CategoryModelSerializer, ProductModelSerializer, \
    ProductImageModelSerializer


# Create your views here.


class RegistrationCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CategoryListAPIViewSet(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    lookup_field = "slug"


class ProductListAPIViewSet(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().prefetch_related("images", "variants")
    serializer_class = ProductModelSerializer
    lookup_field = "slug"


class ProductImageListCreateAPIView(ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageModelSerializer


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apps.models import ProductVariant
from apps.serializers import ProductVariantSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductVariantListCreateAPIView(ListCreateAPIView):
    queryset = ProductVariant.objects.select_related("product").all()
    serializer_class = ProductVariantSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["product", "color", "size", "ram", "storage", "is_available"]
    search_fields = ["product__name", "color", "size", "ram", "storage"]
    ordering_fields = ["price", "stock"]
    ordering = ["-id"]


class ProductVariantDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.select_related("product").all()
    serializer_class = ProductVariantSerializer
    lookup_field = "id"
