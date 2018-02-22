# coding: utf-8
from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'maxlength': '2', 'class': 'form-control'}),
                                  label='Количество', min_value=1, max_value=20, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartAddProductFormAuto(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'maxlength': '2', 'class': 'form-control', 'onchange':'this.form.submit()' }),
                                  label='Количество', min_value=1, max_value=20, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)