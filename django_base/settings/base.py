import os
import json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(BASE_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())

def get_secrets(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured

CSRF_HEADER_NAME = 'HTTP_X_XSRF_TOKEN'
AJAX_API_DOMEN = get_secrets('AJAX_API_DOMEN')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secrets('SECRET_KEY')

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',

    'base',
    'my_auth',
    'pushes',
    'vampire_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pushes.context_processors.push_public_vapid',
                'base.context_processors.ajax_api_domen',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_base.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Custom auth settings
LOGIN_URL = '/my_auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_ATTEMPTS = {
    "15_MINUTES_BLOCK": 3,
    "24_HOURS_BLOCK": 9,
}

AUTH_USER_MODEL = 'my_auth.ConfirmedUser'


EMAIL_HOST = get_secrets('EMAIL')['EMAIL_HOST']
EMAIL_PORT = get_secrets('EMAIL')['EMAIL_PORT']
EMAIL_HOST_USER = get_secrets('EMAIL')['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = get_secrets('EMAIL')['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = get_secrets('EMAIL')['EMAIL_USE_TLS']


VAPID_PRIVATE_KEY = get_secrets('WEBPUSH_SETTINGS')['VAPID_PRIVATE_KEY']
VAPID_PUBLIC_KEY = get_secrets('WEBPUSH_SETTINGS')['VAPID_PUBLIC_KEY']
VAPID_ADMIN_EMAIL = get_secrets('WEBPUSH_SETTINGS')['VAPID_ADMIN_EMAIL']