from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import Category, Product, ProductVariant, ProductImages
from apps.serializers import (
    CategoryModelSerializer,
    ProductModelSerializer,
    ProductVariantModelSerializer,
    ProductImageModelSerializer, RegisterSerializer,
)

User = get_user_model()
class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            password = validated_data.get("password")
            user = User.objects.create(
                email=validated_data.get("email"),
                phone=validated_data.get("phone"),
                password=make_password(password)
            )
            refresh = RefreshToken.for_user(user)
            return Response({
                "message":"Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tdi ✅",
                "user":{
                    "id":user.id,
                    "email":user.email,
                    "phone":user.phone
                },
                "tokens":{
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                }

            },status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    queryset = ProductImages.objects.select_related("product")
    serializer_class = ProductImageModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product__slug", "is_main"]
    search_fields = ["product__name"]


class ProductImagesDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductImages.objects.select_related("product")
    serializer_class = ProductImageModelSerializer
