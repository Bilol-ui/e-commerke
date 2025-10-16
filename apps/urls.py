from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.views import (
    RegistrationCreateAPIView,
    CategoryModelViewSet,
    ProductModelViewSet,
    ProductImageModelViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryModelViewSet, basename="category")
router.register("products", ProductModelViewSet, basename="product")
router.register("product-images", ProductImageModelViewSet, basename="product-image")

urlpatterns = [
    path("register/", RegistrationCreateAPIView.as_view(), name="register"),
    path("", include(router.urls)),
]
