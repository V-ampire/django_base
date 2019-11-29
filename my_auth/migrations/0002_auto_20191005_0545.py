# Generated by Django 2.2.5 on 2019-10-05 05:45

import django.contrib.auth.models
from django.db import migrations, models
import my_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='confirmeduser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
                ('confirmed', my_auth.models.ConfirmedManager()),
            ],
        ),
        migrations.AlterField(
            model_name='confirmeduser',
            name='confirm',
            field=models.BooleanField(default=False, verbose_name='Пользователь подтвержден'),
        ),
    ]