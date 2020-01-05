## Настройки settings.py

REGISTER_TIMEOUT - время жизни ссылкии

Тестирование:
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

AUTH_USER_MODEL = 'my_auth.ConfirmedUser'

SITE_ID = 1

INSTALLED_APPS = [
    ...
    'django.contrib.sites',

    'my_auth',
]


## Best practises

- Для добавления дополнительных методов (не переопределяя существующих) использовать proxy-модели

- В начале проекта определить свою модель пользователя, в случает если не изменяется модель по умолчанию все равно выполнить слдующие действия:

```
# models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)


# settings.py

AUTH_USER_MODEL = 'app.models.User'
```

- Для доступа к модели пользователя использовать `get_user_model` из `django.contrib.auth` 