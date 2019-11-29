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

