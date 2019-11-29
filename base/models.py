from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateField("Дата создания", auto_now_add=True)
    modified = models.DateField("Дата изменения", auto_now=True)

    class Meta:
        abstract = True


class ObjectsOnManager(models.Manager):
    def get_queryset(self):
        return super(ObjectsOnManager, self).get_queryset().filter(status='on')


class OnOffStatusModel(models.Model):
    ON = 'on'
    OFF = 'off'
    STATUS_CHOICES = (
        (ON, 'Показывать'),
        (OFF, 'Не показывать'),
    )
    status = models.CharField("Статус", max_length=15, choices=STATUS_CHOICES, default=ON)
    objects_on = ObjectsOnManager()
    objects = models.Manager()

    class Meta:
        abstract = True