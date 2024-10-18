from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Product, SoldProduct


class ProductCreateForm(forms.ModelForm):
    delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата завоза"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'необязательно'}),
        label="Описание (необязательно)",
        required=False
    )

    class Meta:
        model = Product
        fields = (
            'title',
            'color',
            'image',
            'description',
            'quantity',
            'purchase_price',
            'storage_location',
            'sale_price',
            'delivery_date',
        )


class SoldProductForm(forms.ModelForm):
    sale_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата продажи"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'необязательно'}),
        label="Описание (необязательно)",
        required=False
    )

    class Meta:
        model = SoldProduct
        fields = (
            'quantity',
            'total_price',
            'sale_date',
            'description',
            'status'
        )


class SoldProductUpdateForm(forms.ModelForm):

    class Meta:
        model = SoldProduct
        fields = (
            'quantity',
            'total_price',
            'sale_date',
            'description',
            'status',
        )


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',  # Добавляем метку на русском языке
        widget=forms.TextInput(
            attrs={
                'class': 'form-control custom-form-field',
                'placeholder': 'Введите ваше имя пользователя'
            }
        )
    )
    password = forms.CharField(
        label='Пароль',  # Добавляем метку на русском языке
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control custom-form-field',
                'placeholder': 'Введите ваш пароль'
            }
        )
    )


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', )



