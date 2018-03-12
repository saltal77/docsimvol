# coding: utf-8
from django import forms
from .models import Rating

class RatingCreateForm(forms.ModelForm):
    CHOICES_R = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    rating = forms.ChoiceField(label='Оценка товара', widget=forms.RadioSelect(attrs={'class': 'form-control'}),
                               required=True, choices=CHOICES_R)
    author = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
                             required=True)
    email = forms.RegexField(label='E-mail', regex=r'.+@.+\..+',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), required=True)

    ratingcomment = forms.CharField(label='Отзыв', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Отзыв'}), required=True)

    class Meta:
        model = Rating
        fields = ['rating', 'author', 'email', 'ratingcomment']


class MailCreateForm(forms.Form):
    author = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
                             required=True)
    email = forms.RegexField(label='E-mail', regex=r'.+@.+\..+',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             required=True)
    message = forms.CharField(label='Отзыв', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Сообщение...'}), required=True)

    tlf = forms.RegexField(regex=r'^\d{8,15}$',

                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'телефон в формате 89998887766'}),
                           required=False)
    honey = forms.CharField(widget=forms.HiddenInput(attrs={'value': ''}), required=False)

    class Meta:
        fields = ['author', 'email', 'tlf', 'message']


class MyFilterForm(forms.Form):
    CHOICES_ST = (
        ('Муж', 'Мужские'),
        ('Жен', 'Женские'),
    )
    CHOICES_SP = (
        ('Дороже', 'Дороже'),
        ('Дешевле', 'Дешевле'),
    )

    t = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'option-input radio', 'onchange': 'this.form.submit()'}), choices=CHOICES_ST,
        initial=' ', required=False)
    p = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'option-input radio', 'onchange': 'this.form.submit()'}), choices=CHOICES_SP,
        initial=' ', required=False)
    p_min = forms.RegexField(label='от', regex=r'^\d{1,6}$',
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'maxlength': '6', 'pattern': '\d+', 'placeholder': 'Min',
                                              'onchange': 'this.form.submit()'}), required=False)
    p_max = forms.RegexField(label='до', regex=r'^\d{1,6}$',
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'maxlength': '6', 'pattern': '\d+', 'placeholder': 'Max',
                                              'onchange': 'this.form.submit()'}), required=False)
    c = forms.CharField(widget=forms.HiddenInput(
        attrs={'value': ' ', 'id': 'color'}), required=False)
