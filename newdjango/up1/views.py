from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.forms import modelformset_factory
from .models import Car, CarImage, CarCategory, CarStatus, Booking, CustomUser, Role, Order, PaymentType
from .forms import CarForm, CarImageForm, CarCategoryForm, CarStatusForm, BookingForm, CustomUserForm, RoleForm, OrderForm, PaymentTypeForm, RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
import json
from django.utils.dateformat import format as date_format
from datetime import timedelta
from .decorators import anonymous_required

def is_manager(user):
    return user.is_authenticated and hasattr(user, 'role') and user.role and user.role.name.lower() == 'манагер'


def card_auto(request):
    cars = Car.objects.all()
    form = BookingForm()
    return render(request, 'up1/card_auto.html', {'cars': cars, 'form': form})
def contacts(request):
    return render(request, 'contacts.html')

def home(request):
    return render(request, 'home.html')

def conditions(request):
    return render(request, 'conditions.html')

from django.shortcuts import render
@login_required
@user_passes_test(is_manager)
def manage_categories(request):
    return render(request, 'admin/manage_categories.html')

def manage_statuses(request):
    return render(request, 'admin/manage_statuses.html')

def manage_bookings(request):
    return render(request, 'admin/manage_bookings.html')

def manage_users(request):
    return render(request, 'admin/manage_users.html')

def manage_roles(request):
    return render(request, 'admin/manage_roles.html')

def manage_orders(request):
    return render(request, 'admin/manage_orders.html')

def manage_payment_types(request):
    return render(request, 'admin/manage_payment_types.html')

@login_required
def add_to_my_bookings(request, car_id):
    response = redirect('my_bookings')  # редирект на страницу со списком
    my_bookings = request.COOKIES.get('my_bookings', '')
    ids = [i for i in my_bookings.split(',') if i.isdigit()]
    
    if str(car_id) not in ids:
        ids.append(str(car_id))

    response.set_cookie('my_bookings', ','.join(ids), max_age=60*60*24*30)  # 30 дней
    return response


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user/my_bookings.html', {'bookings': bookings})


@login_required
def my_orders(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user/my_orders.html', {'bookings': bookings})


@user_passes_test(is_manager, login_url='home') 
def custom_admin(request):
    cars = Car.objects.all().prefetch_related('images')
    statuses = CarStatus.objects.all()

    year = request.GET.get("year")
    status = request.GET.get("status")
    brand = request.GET.get("brand")
    query = request.GET.get("q")
    sort_by = request.GET.get("sort")

    if year:
        cars = cars.filter(year=year)
    if status:
        cars = cars.filter(status_id=status)
    if brand:
        cars = cars.filter(brand__icontains=brand)
    if query:
        cars = cars.filter(Q(model__icontains=query) | Q(description__icontains=query))

    ALLOWED_SORT_FIELDS = ['daily_price', '-daily_price', 'model', '-model', 'year', '-year']
    if sort_by in ALLOWED_SORT_FIELDS:
        cars = cars.order_by(sort_by)

    context = {
        'cars': cars,
        'statuses': statuses,
    }
    return render(request, 'admin_panel.html', context)


def add_car(request):
    CarImageFormSet = modelformset_factory(CarImage, form=CarImageForm, extra=3, can_delete=False)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        formset = CarImageFormSet(request.POST, request.FILES, queryset=CarImage.objects.none())
        if form.is_valid() and formset.is_valid():
            car = form.save()

            # Сохраняем новые изображения
            for img_form in formset:
                if img_form.cleaned_data and not img_form.cleaned_data.get('DELETE', False):
                    image_instance = img_form.save(commit=False)
                    image_instance.car = car
                    image_instance.save()

            return redirect('custom_admin')

    else:
        form = CarForm()
        formset = CarImageFormSet(queryset=CarImage.objects.none())

    return render(request, 'car_form.html', {'form': form, 'formset': formset})


def edit_car(request, pk):
    car = Car.objects.get(pk=pk)
    CarImageFormSet = modelformset_factory(CarImage, form=CarImageForm, extra=3, can_delete=True)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        formset = CarImageFormSet(request.POST, request.FILES, queryset=CarImage.objects.filter(car=car))

        if form.is_valid() and formset.is_valid():
            form.save()

            # Удаляем отмеченные для удаления изображения
            for form_img in formset:
                if form_img.cleaned_data.get('DELETE', False) and form_img.instance.pk:
                    form_img.instance.delete()

            # Сохраняем новые и обновленные изображения
            instances = formset.save(commit=False)
            for instance in instances:
                instance.car = car
                instance.save()

            return redirect('custom_admin')

        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)

    else:
        form = CarForm(instance=car)
        formset = CarImageFormSet(queryset=CarImage.objects.filter(car=car))

    return render(request, 'car_form.html', {'form': form, 'formset': formset})


def delete_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    car.delete()
    return redirect('custom_admin')



# Список категорий
def category_list(request):
    return render(request, 'admin/generic_list.html', {
        'title': 'Категории авто',
        'items': CarCategory.objects.all(),
        'headers': ['ID', 'Название'],
        'fields': ['id', 'name'],
        'add_url': 'category_create',
        'edit_url': 'category_edit',
        'delete_url': 'category_delete',
    })

def category_create(request):
    form = CarCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'common/form.html', {
        'form': form,
        'title': 'Добавить категорию',
        'back_url': 'category_list',
    })


def category_edit(request, pk):
    category = get_object_or_404(CarCategory, pk=pk)
    form = CarCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'common/form.html', {
        'form': form,
        'title': 'Редактировать категорию',
        'back_url': 'category_list',
    })


def category_delete(request, pk):
    category = get_object_or_404(CarCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'common/confirm_delete.html', {'object': category})






# Список
def status_list(request):
    statuses = CarStatus.objects.all()
    return render(request, 'admin/generic_list.html', {
        'title': 'Статусы авто',
        'items': statuses,
        'headers': ['ID', 'Название'],
        'fields': ['id', 'name'],
        'add_url': 'status_create',
        'edit_url': 'status_edit',
        'delete_url': 'status_delete',
    })
# Создание
def status_create(request):
    form = CarStatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('status_list')
    return render(request, 'common/form.html', {
        'form': form,
        'title': 'Добавить статус',
        'back_url': 'status_list',
    })
# Редактирование
def status_edit(request, pk):
    status = get_object_or_404(CarStatus, pk=pk)
    form = CarStatusForm(request.POST or None, instance=status)
    if form.is_valid():
        form.save()
        return redirect('status_list')
    return render(request, 'common/form.html', {
        'form': form,
        'title': 'Редактировать статус',
        'back_url': 'status_list',
    })
# Удаление
def status_delete(request, pk):
    status = get_object_or_404(CarStatus, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('status_list')
    return render(request, 'common/confirm_delete.html', {'object': status})




# Список бронирований
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'admin/generic_list.html', {
        'title': 'Бронирования',
        'items': bookings,
        'headers': ['ID', 'Авто', 'Пользователь', 'Начало', 'Конец', 'Сумма'],
        'fields': ['id', 'car', 'user', 'start_date', 'end_date', 'total_price'],
        'add_url': 'booking_create',
        'edit_url': 'booking_edit',
        'delete_url': 'booking_delete',
    })

@login_required(login_url='login')
def booking_create(request):
    car_id = request.GET.get('car') or request.POST.get('car')
    car = get_object_or_404(Car, pk=car_id)

    # Получаем занятые даты по бронированиям автомобиля
    bookings = Booking.objects.filter(car=car)
    busy_dates = []
    for b in bookings:
        current_date = b.start_date
        while current_date <= b.end_date:
            busy_dates.append(current_date.isoformat())
            current_date += timedelta(days=1)

    busy_dates_json = json.dumps(busy_dates)

    # остальной код
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.user = request.user
            start_date = booking.start_date
            end_date = booking.end_date

            overlapping_bookings = Booking.objects.filter(
                car=car,
                start_date__lte=end_date,
                end_date__gte=start_date,
            )

            if overlapping_bookings.exists():
                messages.error(request, "Выбранные даты уже заняты. Пожалуйста, выберите другие.")
            else:
                days = (end_date - start_date).days
                if days < 1:
                    days = 1
                booking.total_price = days * car.daily_price
                booking.save()
                return redirect('booking_payment', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'booking/booking_form.html', {
        'form': form,
        'car': car,
        'busy_dates_json': busy_dates_json,
    })


@login_required
def booking_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    payment_types = PaymentType.objects.all()

    if request.method == 'POST':
        payment_type_id = request.POST.get('payment_type')
        if payment_type_id:
            payment_type = PaymentType.objects.get(id=payment_type_id)

            # Создаём заказ
            Order.objects.create(
                booking=booking,
                payment_type=payment_type,
                total=booking.total_price
            )

            return redirect('payment_success')  

    return render(request, 'booking/booking_payment.html', {
        'booking': booking,
        'payment_types': payment_types
    })

def payment_success(request):
    return render(request, 'booking/payment_success.html')

# Редактирование
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        return redirect('booking_list')
    return render(request, 'common/form.html', {
        'form': form,
        'title': 'Редактировать бронирование',
        'back_url': 'booking_list',
    })

# Удаление
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'common/confirm_delete.html', {'object': booking})



# Список пользователей
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/generic_list.html', {
        'title': 'Пользователи',
        'items': users,
        'headers': ['ID', 'Имя', 'Фамилия', 'Телефон', 'Логин', 'Документ', 'Роль'],
        'fields': ['id', 'first_name', 'last_name', 'phone', 'login', 'document_number', 'role'],
        'add_url': 'user_create',
        'edit_url': 'user_edit',
        'delete_url': 'user_delete',
    })

# Создание
def user_create(request):
    form = CustomUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, 'common/form.html', {
        'form': form,
        'title': 'Новый пользователь',
        'back_url': 'user_list',
    })

# Редактирование
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    form = CustomUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, 'common/form.html', {
        'form': form,
        'title': 'Редактировать пользователя',
        'back_url': 'user_list',
    })

# Удаление
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'common/confirm_delete.html', {'object': user})




def role_list(request):
    roles = Role.objects.all()
    return render(request, 'admin/generic_list.html', {
        'title': 'Роли',
        'items': roles,
        'headers': ['ID', 'Название'],
        'fields': ['id', 'name'],
        'add_url': 'role_create',
        'edit_url': 'role_edit',
        'delete_url': 'role_delete'
    })

def role_create(request):
    form = RoleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('role_list')
    return render(request, 'common/form.html', {'form': form, 'title': 'Добавить роль', 'back_url': 'role_list'})

def role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)
    form = RoleForm(request.POST or None, instance=role)
    if form.is_valid():
        form.save()
        return redirect('role_list')
    return render(request, 'common/form.html', {'form': form, 'title': 'Редактировать роль', 'back_url': 'role_list'})

def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('role_list')
    return render(request, 'common/confirm_delete.html', {'object': role, 'back_url': 'role_list'})



def order_list(request):
    orders = Order.objects.all()
    return render(request, 'admin/generic_list.html', {
        'title': 'Заказы',
        'items': orders,
        'headers': ['ID', 'Бронирование', 'Тип оплаты', 'Сумма'],
        'fields': ['id', 'booking', 'payment_type', 'total'],
        'add_url': 'order_create',
        'edit_url': 'order_edit',
        'delete_url': 'order_delete'
    })

def order_create(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('order_list')
    return render(request, 'common/form.html', {'form': form, 'title': 'Добавить заказ', 'back_url': 'order_list'})

def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('order_list')
    return render(request, 'common/form.html', {'form': form, 'title': 'Редактировать заказ', 'back_url': 'order_list'})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'common/confirm_delete.html', {'object': order, 'back_url': 'order_list'})





def paymenttype_list(request):
    payment_types = PaymentType.objects.all()
    return render(request, 'admin/generic_list.html', {
        'title': 'Типы оплаты',
        'items': payment_types,
        'headers': ['ID', 'Название'],
        'fields': ['id', 'name'],
        'add_url': 'paymenttype_create',
        'edit_url': 'paymenttype_edit',
        'delete_url': 'paymenttype_delete',
    })

def paymenttype_create(request):
    form = PaymentTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('paymenttype_list')
    return render(request, 'common/form.html', {'form': form, 'title': 'Добавить тип оплаты', 'back_url': 'paymenttype_list'})

def paymenttype_edit(request, pk):
    payment_type = get_object_or_404(PaymentType, pk=pk)
    form = PaymentTypeForm(request.POST or None, instance=payment_type)
    if form.is_valid():
        form.save()
        return redirect('paymenttype_list')
    return render(request, 'common/form.html', {'form': form, 'title': 'Редактировать тип оплаты', 'back_url': 'paymenttype_list'})

def paymenttype_delete(request, pk):
    payment_type = get_object_or_404(PaymentType, pk=pk)
    if request.method == 'POST':
        payment_type.delete()
        return redirect('paymenttype_list')
    return render(request, 'common/confirm_delete.html', {'object': payment_type, 'back_url': 'paymenttype_list'})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # куда редиректить после входа
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
