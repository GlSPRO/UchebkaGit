from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from .views import register_view

urlpatterns = [
    path('', views.home, name='home'),
    path('conditions/', views.conditions, name='conditions'),
    path('contacts/', views.contacts, name='contacts'),
    path('card_auto/', views.card_auto, name='card_auto'),
    path('car/add/', views.add_car, name='add_car'),
    path('car/<int:pk>/edit/', views.edit_car, name='edit_car'),
    path('car/<int:pk>/delete/', views.delete_car, name='delete_car'),

    path('admin_panel/', views.custom_admin, name='custom_admin'),

    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('add-to-my-bookings/<int:car_id>/', views.add_to_my_bookings, name='add_to_my_bookings'),
    path('payment-success/', views.payment_success, name='payment_success'),  # Добавь обработчик

    path('my-orders/', views.my_orders, name='my_orders'),

    path('login/', LoginView.as_view(template_name='auth/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_view, name='register'),

    # CRUD для всех таблиц
    path('category/', views.category_list, name='category_list'),
    path('category/add/', views.category_create, name='category_create'),
    path('category/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('status/', views.status_list, name='status_list'),
    path('status/create/', views.status_create, name='status_create'),
    path('status/<int:pk>/edit/', views.status_edit, name='status_edit'),
    path('status/<int:pk>/delete/', views.status_delete, name='status_delete'),


    path('booking/', views.booking_list, name='booking_list'),
    path('booking/create/', views.booking_create, name='booking_create'),
    path('booking/<int:pk>/edit/', views.booking_edit, name='booking_edit'),
    path('booking/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('booking/payment/<int:booking_id>/', views.booking_payment, name='booking_payment'),

    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    path('roles/', views.role_list, name='role_list'),
    path('roles/add/', views.role_create, name='role_create'),
    path('roles/<int:pk>/edit/', views.role_edit, name='role_edit'),
    path('roles/<int:pk>/delete/', views.role_delete, name='role_delete'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.order_create, name='order_create'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    path('payments/', views.paymenttype_list, name='paymenttype_list'),
    path('payments/add/', views.paymenttype_create, name='paymenttype_create'),
    path('payments/<int:pk>/edit/', views.paymenttype_edit, name='paymenttype_edit'),
    path('payments/<int:pk>/delete/', views.paymenttype_delete, name='paymenttype_delete'),


]
