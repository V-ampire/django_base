from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
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