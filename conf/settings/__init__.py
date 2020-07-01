import datetime
import os
from pathlib import Path
from decouple import config
from dj_database_url import parse as db_url

from .celery import *
from .celerybeat import *
from .email import *
from .external import *
from .monitoring import *
from .logging import *
from .rest_framework import *


DEBUG = config('DEBUG', default=False, cast=bool)

ENVIRONMENT = config('ENVIRONMENT')
SECRET_KEY = config('SECRET_KEY', default='')

BASE_DIR = Path(__file__).parent.parent.parent

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'django_celery_beat',
]

LOCAL_APPS = []

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'utils.helpers.structlog.StructlogMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'
SITE_ID = 1

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
            ],
        },
    },
]

ASGI_APPLICATION = "common.routing.application"
WSGI_APPLICATION = 'conf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': dict(config('DATABASE_URL', cast=db_url), TEST={'SERIALIZE': False, 'NAME': 'test_db'})
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
# AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
)

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/admin/login/'
LOGOUT_URL = '/admin/logout/'

# SECURE
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# files
MAX_FILE_UPLOAD_SIZE = 50 * 1024 * 1024
FILE_UPLOAD_PERMISSIONS = 0o644

VALID_FILE_UPLOAD_ALL_EXTENSIONS = [
    'jpg',
    'jpeg',
    'png',
    'bmp',
]

# Environment conditions
if ENVIRONMENT == 'prod':
    ALLOWED_HOSTS = ['my.local.app', 'api.local.app']

elif ENVIRONMENT == 'stage':
    ALLOWED_HOSTS = ['dev.my.local.app', 'dev.api.local.app']

    from .debugtoolbar import *

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
elif ENVIRONMENT == 'dev':
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

    from .debugtoolbar import *

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
elif ENVIRONMENT == 'test':
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
