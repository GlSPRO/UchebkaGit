from rest_framework import viewsets, mixins, filters
from up1.models import (
    CarCategory, CarStatus, Car, Role, CustomUser,
    Booking, PaymentType, Order, Review, CarImage
)
from api.serializers import (
    CarCategorySerializer, CarStatusSerializer, CarSerializer,
    RoleSerializer, CustomUserSerializer, BookingSerializer,
    PaymentTypeSerializer, OrderSerializer, ReviewSerializer,
    CarImageSerializer
)
from .permissons import CustomPermissions, Pagination
from rest_framework.renderers import AdminRenderer

# --- Категория авто ---
class CarCategoryViewSet(viewsets.ModelViewSet):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategorySerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

# --- Статус автомобиля ---
class CarStatusViewSet(viewsets.ModelViewSet):
    queryset = CarStatus.objects.all()
    serializer_class = CarStatusSerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

# --- Автомобили ---
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['brand']  # Поиск по бренду автомобиля

# --- Фото автомобилей ---
class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['image']  # Поиск по имени файла изображения

# --- Роли ---
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

# --- Пользователи ---
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    renderer_classes = [AdminRenderer]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name']

# --- Бронирование ---
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['car__brand']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return Booking.objects.none()

# --- Типы оплаты ---
class PaymentTypeViewSet(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

# --- Заказы ---
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['booking__car__brand']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(booking__user=user)
        return Order.objects.none()

# --- Отзывы ---
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomPermissions]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['text']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return Review.objects.none()
