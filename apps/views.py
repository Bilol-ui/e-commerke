from apps.models import Category, Product, ProductImages, ProductVariant
from apps.models.banners import Banner
from apps.paginations import Pagination
from apps.permissions import RoleBasedPermission
from apps.serializers import (
    BannerModelSerializer,
    CategoryModelSerializer,
    ProductImageModelSerializer,
    ProductModelSerializer,
    ProductVariantModelSerializer,
    RegisterSerializer,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# @extend_schema(tags=['Auth'])
# class RegisterAPIView(CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             validated_data = serializer.validated_data
#             password = validated_data.get("password")
#             user = User.objects.create(
#                 email=validated_data.get("email"),
#                 phone=validated_data.get("phone"),
#                 password=make_password(password)
#             )
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "message": "Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tdi ✅",
#                 "user": {
#                     "id": user.id,
#                     "email": user.email,
#                     "phone": user.phone
#                 },
#                 "tokens": {
#                     "refresh": str(refresh),
#                     "access": str(refresh.access_token),
#                 }
#
#             }, status=status.HTTP_201_CREATED)
#         except ValidationError as e:
#             return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Auth'],
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=RegisterSerializer,
            description="Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tdi ✅",
            examples=[
                OpenApiExample(
                    'Successful Register',
                    summary='Example of success response',
                    description='Bu foydalanuvchi ro‘yxatdan o‘tgandan keyingi javob ko‘rinishi',
                    value={
                        "message": "Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tdi ✅",
                        "user": {
                            "id": 1,
                            "email": "example@gmail.com",
                            "phone": "+998901234567"
                        },
                        "tokens": {
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                                       "SmDN9hhTOlbQp7CFJF11401EHd7BT66LkCDORTyG5B0",
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                                      "NN3G8iRmEyLbYuH_yz-EgVJTYwwp3cbCFZ_Ynez5CyQ"
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Validatsiya xatosi",
            examples=[
                OpenApiExample(
                    'Validation Error',
                    value={"errors": {"email": ["Bu email allaqachon ro‘yxatdan o‘tgan."]}}
                )
            ]
        ),
        500: OpenApiResponse(
            description="Server xatosi",
            examples=[
                OpenApiExample(
                    'Server Error',
                    value={"error": "Something went wrong"}
                )
            ]
        ),
    }
)
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
                "message": "Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tdi ✅",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "phone": user.phone
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }

            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]
    permission_classes = [IsAuthenticated, AllowAny]
    pagination_class = Pagination
    authentication_classes = []


# class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializer
#     lookup_field = "slug"


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().select_related("category")
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "name"]
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    pagination_class = Pagination
    authentication_classes = []


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductModelSerializer
    lookup_field = "slug"


class ProductVariantListCreateAPIView(ListCreateAPIView):
    queryset = ProductVariant.objects.select_related("product")
    serializer_class = ProductVariantModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product__slug", "color", "size", "ram", "storage", "is_available"]
    search_fields = ["product__name"]
    pagination_class = Pagination


class ProductVariantDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.select_related("product")
    serializer_class = ProductVariantModelSerializer


class ProductImagesListCreateAPIView(ListCreateAPIView):
    queryset = ProductImages.objects.select_related("product")
    serializer_class = ProductImageModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product__slug", "is_main"]
    search_fields = ["product__name"]
    pagination_class = Pagination


class ProductImagesDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductImages.objects.select_related("product")
    serializer_class = ProductImageModelSerializer


class BannerListCreateAPIView(ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerModelSerializer
    permission_classes = [IsAuthenticated, AllowAny]  # barcha foydalanuvchilar ko'ra oladi
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    authentication_classes = []


