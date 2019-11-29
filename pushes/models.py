from base.models import TimeStampedModel
from django.contrib.postgres.fields import JSONField
from django.db import models


class Subscription(TimeStampedModel):
    # FIXME Добавить ссылку на текущую модель юзера
    # FIXME  Проверять во вью если пользователь зарегался обновить модель подписки
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscription = JSONField(unique=True)
    browser = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return 'subscribe from {}'.format(self.browser)
