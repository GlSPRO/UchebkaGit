from django import forms
from .models import Car, CarImage, CarCategory, CarStatus, Booking, CustomUser, Role, Order, PaymentType
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

# Общий стиль для всех input
input_style = {'class': 'form-control'}
select_style = {'class': 'form-select'}

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs=input_style),
            'category': forms.Select(attrs=select_style),
            'status': forms.Select(attrs=select_style),
            'price_per_day': forms.NumberInput(attrs=input_style),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

class CarCategoryForm(forms.ModelForm):
    class Meta:
        model = CarCategory
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs=input_style),
        }

class CarStatusForm(forms.ModelForm):
    class Meta:
        model = CarStatus
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs=input_style),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'login', 'document_number', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs=input_style),
            'last_name': forms.TextInput(attrs=input_style),
            'phone': forms.TextInput(attrs=input_style),
            'login': forms.TextInput(attrs=input_style),
            'document_number': forms.TextInput(attrs=input_style),
            'role': forms.Select(attrs=select_style),
        }

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs=input_style),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['booking', 'payment_type', 'total']
        widgets = {
            'booking': forms.Select(attrs=select_style),
            'payment_type': forms.Select(attrs=select_style),
            'total': forms.NumberInput(attrs=input_style),
        }

class PaymentTypeForm(forms.ModelForm):
    class Meta:
        model = PaymentType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs=input_style),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'login', 'document_number', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')  # это будет поле login
