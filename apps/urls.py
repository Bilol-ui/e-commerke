from django.urls import path

from .views import (

    BannerListCreateAPIView,
    CategoryListCreateAPIView,
    ProductDetailAPIView,
    ProductListCreateAPIView,
    ProductVariantDetailAPIView,
    ProductVariantListCreateAPIView,
    RegisterAPIView, CartListCreateAPIView,
    CartItemListCreateAPIView,
    WishlistCreateAPIView,
    OrderListCreateViewSet,
OrderHistoryListCreateAPIView,
)

urlpatterns = [
    path("register", RegisterAPIView.as_view(), name="register"),
    path("categories", CategoryListCreateAPIView.as_view(), name="category-list"),


    path("products", ProductListCreateAPIView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),

    path("variants", ProductVariantListCreateAPIView.as_view(), name="variant-list"),
    path("variants/<int:pk>/", ProductVariantDetailAPIView.as_view(), name="variant-detail"),
    path('banners', BannerListCreateAPIView.as_view(), name='banner-list'),
    path('carts',CartListCreateAPIView.as_view(),name='cart-list'),
    path('cart_items',CartItemListCreateAPIView.as_view(),name='carts-items'),
    path('wishlist',WishlistCreateAPIView.as_view(),name='wishlist'),
    path('orders',OrderListCreateViewSet.as_view(),name='orders-list'),
    path('order_history',OrderHistoryListCreateAPIView.as_view(),name='order-history')

]
