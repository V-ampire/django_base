from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, \
    AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.sites.models import Site
from django.template import loader
from .utils import get_temp_url_token


class TemporaryBanIP(models.Model):
    """
        Забаненный IP за большое количесвто попыток входа
    """ 
    ip_address = models.GenericIPAddressField("IP адрес")
    attempts = models.IntegerField("Неудачных попыток", default=0)
    time_unblock = models.DateTimeField("Время разблокировки", blank=True)
    status = models.BooleanField("Статус блокировки", default=False)

    def __str__(self):
        return self.ip_address


class ConfirmedManager(UserManager):
    def get_queryset(self):
        return super(ConfirmedManager, self).get_queryset().filter(confirm=True)


class ConfirmedUser(AbstractUser):
    """
        Модель пользователя с флагом и методом подтверждения, расширяет абстрактную модель
    """
    # Шаблоны для письма подтверждения
    confirm_email_subject_template = 'my_auth/register/confirm_email_subject.txt'
    confirm_email_template = 'my_auth/register/confirm_email_email.html'
    
    # Поля модели
    email = models.EmailField("Email пользователя", max_length=128, unique=True)
    confirm = models.BooleanField("Пользователь подтвержден", default=False)
    # Менеджеры
    objects = UserManager()
    confirmed = ConfirmedManager()

    def send_confirmation(self, use_https=True):
        if not self.confirm:
            domain = Site.objects.get_current().domain
            subject = loader.render_to_string(
                self.confirm_email_subject_template, {'domain': domain}
            )
            context = {
                'protocol': 'https' if use_https else 'http',
                'domain': domain,
                'token': get_temp_url_token(self)
            }
            message = loader.render_to_string(self.confirm_email_template, context)
            self.email_user(subject, message)


class CustomUserManager(BaseUserManager):
    """Менеджер для CustomConfirmedUser, для superuser не требуется подтверждения имейла и имейл не обязателен"""

    def create_user(username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('confirm', False)
        if not username or not email:
            raise ValueError("Users must have username and email address")

        user = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('confirm', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        user = self.create_user(
            username,
            email,
            password=password,
            **extra_fields
        )
        user.save(using=self._db)
        return user


class CustomConfirmedManager(CustomUserManager):
    """Менеджер для обращения только к подтвержденным пользователям"""

    def get_queryset(self):
        return super(CustomConfirmedManager, self).get_queryset().filter(confirm=True)


class CustomConfirmedUser(AbstractBaseUser, PermissionsMixin):
    """Модель юзера с опцией подтверждени по имеил, наследуется от AbstractBaseUser"""

    email = models.EmailField("Email пользователя", max_length=128, unique=True)
    username = models.CharField("Логин пользователя", max_length=128, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    confirm = models.BooleanField("Пользователь подтвержден", default=False)

    objects = CustomUserManager()
    confirmed = CustomConfirmedManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username
    