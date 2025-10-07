from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.views import RegistrationCreateAPIView, ProductViewSet, ProductImageViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'product-images', ProductImageViewSet, basename='product-images')

urlpatterns = [
    path('register/', RegistrationCreateAPIView.as_view(), name='register'),
    path('', include(router.urls)),
]
