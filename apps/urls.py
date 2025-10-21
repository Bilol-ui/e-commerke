from django.urls import path
from .views import (
    RegistrationCreateAPIView,
    CategoryListAPIViewSet,
    CategoryDetailAPIView,
    ProductListAPIViewSet,
    ProductDetailAPIView,
    ProductImageListCreateAPIView,
)

urlpatterns = [
    path("register/", RegistrationCreateAPIView.as_view(), name="register"),

    path("categories/", CategoryListAPIViewSet.as_view(), name="category-list"),

    path("categories/<slug:slug>/", CategoryDetailAPIView.as_view(), name="category-detail"),

    path("products/", ProductListAPIViewSet.as_view(), name="product-list"),

    path("products/<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),

    path("product-images/", ProductImageListCreateAPIView.as_view(), name="product-image-list-create"),
]
