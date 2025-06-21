from django.contrib import admin
from .models import (
    Car, CarCategory, CarStatus, CarImage,
    Role, CustomUser, Booking, PaymentType, Order, Review
)


@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(CarStatus)
class CarStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'year', 'daily_price', 'category', 'status')
    list_filter = ('status', 'category')
    search_fields = ('brand', 'model')


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'image')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'login', 'role')
    search_fields = ('first_name', 'last_name', 'login')
    list_filter = ('role',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'user', 'start_date', 'end_date', 'total_price')
    list_filter = ('start_date', 'end_date')
    search_fields = ('car__brand', 'user__first_name')


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'payment_type', 'total')
    list_filter = ('payment_type',)
    search_fields = ('booking__user__first_name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'user', 'rating')
    search_fields = ('car__brand', 'user__first_name')
