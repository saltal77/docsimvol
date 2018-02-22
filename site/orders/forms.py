# coding: utf-8
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    tlf = forms.RegexField(regex=r'^\d{8,15}$', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.RegexField(regex=r'.+@.+\..+', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    delivery = forms.BooleanField(initial=False, required=False)


    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'tlf', 'city', 'comment', 'delivery']
