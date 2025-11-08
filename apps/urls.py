from django.urls import path

from .views import (
    RegisterAPIView,
    CategoryListCreateAPIView,
    ProductListCreateAPIView, ProductDetailAPIView,
    ProductVariantListCreateAPIView, ProductVariantDetailAPIView,
BannerListCreateAPIView,BannerDetailAPIView
)

urlpatterns = [
    path("register", RegisterAPIView.as_view(), name="register"),
    path("categories", CategoryListCreateAPIView.as_view(), name="category-list"),


    path("products", ProductListCreateAPIView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),

    path("variants", ProductVariantListCreateAPIView.as_view(), name="variant-list"),
    path("variants/<int:pk>/", ProductVariantDetailAPIView.as_view(), name="variant-detail"),
    path('banners', BannerListCreateAPIView.as_view(), name='banner-list'),
    path('banners/<int:pk>/', BannerDetailAPIView.as_view(), name='banner-detail'),
    # path("images", ProductImagesListCreateAPIView.as_view(), name="image-list"),
    # path("images/<int:pk>/", ProductImagesDetailAPIView.as_view(), name="image-detail"),
]
