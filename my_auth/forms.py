from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from my_auth.models import ConfirmedUser


class ConfirmedUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=128,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
        }))
    class Meta(UserCreationForm.Meta):
        model = ConfirmedUser
        fields = ("username", "email")


class ConfirmedUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ConfirmedUser


class ResendConfirmForm(forms.Form):
    email = forms.EmailField(
        max_length=128,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
        }))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not ConfirmedUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email не зарегистрирован.')
        return email


class LoginForm(AuthenticationForm):
    """
        Форма для входа в систему
    """
    username = forms.CharField(label="Ваш логин:", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'id_username',
        'placeholder': 'Введите логин'
    }))
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'id_password',
        'placeholder': 'Введите пароль'
    }))

    