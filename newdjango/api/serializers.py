from rest_framework import serializers
from up1.models import (
    CarCategory, CarStatus, Car, Role, CustomUser,
    Booking, PaymentType, Order, Review, CarImage
)
from decimal import Decimal


# --- Категория авто ---
class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = ['id', 'name', 'description']


# --- Статус авто ---
class CarStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarStatus
        fields = ['id', 'name']


# --- Фото автомобиля ---
class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image']


# --- Карточка авто ---
class CarSerializer(serializers.ModelSerializer):
    category = CarCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=CarCategory.objects.all(), source='category', write_only=True)

    status = CarStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(queryset=CarStatus.objects.all(), source='status', write_only=True)

    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'brand', 'model', 'year', 'daily_price',
            'category', 'category_id',
            'status', 'status_id',
            'images'
        ]


# --- Роль ---
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


# --- Пользователь ---
class CustomUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'phone', 'login',
            'document_number', 'role', 'role_id'
        ]


# --- Бронирование ---
class BookingSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), source='car', write_only=True)

    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user', write_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'car', 'car_id', 'user', 'user_id',
            'start_date', 'end_date', 'total_price'
        ]


# --- Тип оплаты ---
class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'name']


# --- Заказ ---
class OrderSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    booking_id = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all(), source='booking', write_only=True)

    payment_type = PaymentTypeSerializer(read_only=True)
    payment_type_id = serializers.PrimaryKeyRelatedField(queryset=PaymentType.objects.all(), source='payment_type', write_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'booking', 'booking_id',
            'payment_type', 'payment_type_id',
            'total'
        ]


# --- Отзыв ---
class ReviewSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), source='car', write_only=True)

    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user', write_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'car', 'car_id',
            'user', 'user_id',
            'rating', 'text'
        ]
