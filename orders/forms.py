from django import forms

from orders.models import Order
from django.views.generic.base import TemplateView


class OrdersForm(forms.ModelForm, TemplateView):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Иван'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Иванов'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'you@example.com'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Россия, Москва, ул. Мира, дом 6'
    }))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
