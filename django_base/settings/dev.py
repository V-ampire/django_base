from .base import *

DEBUG = True

ALLOWED_HOSTS = get_secrets('ALLOWED_HOSTS')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secrets('DATABASE')['NAME'],
        'USER' : get_secrets('DATABASE')['USER'],
        'PASSWORD' : get_secrets('DATABASE')['PASSWORD'],
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


REGISTER_TIMEOUT = 5

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'