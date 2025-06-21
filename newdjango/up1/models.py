# up1/models.py
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# --- Категория авто ---
class CarCategory(models.Model):
    name = models.CharField("Категория авто", max_length=100)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name


# --- Статус автомобиля ---
class CarStatus(models.Model):
    name = models.CharField("Статус", max_length=50)

    def __str__(self):
        return self.name


# --- Карточка авто ---
class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey('CarStatus', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.brand} {self.model}"


# --- Роли пользователей ---
class Role(models.Model):
    name = models.CharField("Название роли", max_length=50)

    def __str__(self):
        return self.name


# --- Пользователи ---
class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('Пользователь должен иметь логин')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    login = models.CharField("Логин", max_length=50, unique=True)
    document_number = models.CharField("Номер документа", max_length=50)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, verbose_name="Роль")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# --- Бронирование ---
class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Авто")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    start_date = models.DateField("Дата начала аренды")
    end_date = models.DateField("Дата конца аренды")
    total_price = models.DecimalField("Сумма", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Бронь #{self.id} — {self.car}"


# --- Типы оплаты ---
class PaymentType(models.Model):
    name = models.CharField("Тип оплаты", max_length=50)

    def __str__(self):
        return self.name


# --- Заказы ---
class Order(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Бронирование")
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True, verbose_name="Тип оплаты")
    total = models.DecimalField("Сумма", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Заказ #{self.id}"


# --- Отзывы ---
class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Авто")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.PositiveIntegerField("Оценка")
    text = models.TextField("Текст отзыва")

    def __str__(self):
        return f"Отзыв #{self.id} на {self.car}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')

    def delete(self, *args, **kwargs):
        # Удаляем файл с диска, если он существует
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)