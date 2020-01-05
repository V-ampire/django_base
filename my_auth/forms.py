from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from my_auth.models import ConfirmedUser, CustomConfirmedUser


class ConfirmedUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=128,
        widget=forms.EmailInput(attrs={
            'placeholder': 'email',
        }))
    class Meta(UserCreationForm.Meta):
        model = ConfirmedUser
        fields = ("username", "email")


class ConfirmedUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ConfirmedUser


class CustomConfirmedUserCreationForm(forms.ModelForm):
    """Форма для создания CustomConfirmedUser"""
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput())

    class Meta:
        model = CustomConfirmedUser
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают!')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomConfirmedUserChangeForm(forms.ModelForm):
    """Форма для редактирования CustomConfirmedUser"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomConfirmedUser
        fields = '__all__'

    def clean_password(self):
        return self.initial['password']


class ResendConfirmForm(forms.Form):
    email = forms.EmailField(
        max_length=128,
        widget=forms.EmailInput(attrs={
            'placeholder': 'email',
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

    