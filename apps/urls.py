from django.urls import path
from .views import (
    CategoryListCreateAPIView, CategoryDetailAPIView,
    ProductListCreateAPIView, ProductDetailAPIView,
    ProductVariantListCreateAPIView, ProductVariantDetailAPIView,
    ProductImagesListCreateAPIView, ProductImagesDetailAPIView
)

urlpatterns = [
    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list"),
    path("categories/<slug:slug>/", CategoryDetailAPIView.as_view(), name="category-detail"),

    path("products", ProductListCreateAPIView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),

    path("variants", ProductVariantListCreateAPIView.as_view(), name="variant-list"),
    path("variants/<int:pk>/", ProductVariantDetailAPIView.as_view(), name="variant-detail"),

    path("images", ProductImagesListCreateAPIView.as_view(), name="image-list"),
    path("images/<int:pk>/", ProductImagesDetailAPIView.as_view(), name="image-detail"),
]
