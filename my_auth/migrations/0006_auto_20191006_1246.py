# Generated by Django 2.2.5 on 2019-10-06 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0005_auto_20191005_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmeduser',
            name='email',
            field=models.EmailField(max_length=128, unique=True, verbose_name='Email пользователя'),
        ),
    ]