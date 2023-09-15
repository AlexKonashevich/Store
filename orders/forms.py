from django import forms
from django.db import models
from orders.models import Order
from users.models import User
from django.views.generic.base import TemplateView
from users.forms import UserProfileForm
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
    # model = User
    # form_class = UserProfileForm
    # template_name = 'users/profile.html'
    # title = 'Store - Личный кабинет'
    def get_context_data(self, **kwargs):
        context = super(OrdersForm, self).get_context_data()
        return context

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
