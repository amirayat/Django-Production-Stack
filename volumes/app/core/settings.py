"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import ast
from pathlib import Path
from dotenv import load_dotenv
from distutils.util import strtobool

# project environment variables
# https://pypi.org/project/python-dotenv/
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')
REDIS_USER = os.getenv('REDIS_USER')
REDIS_PASS = os.getenv('REDIS_PASS')

DJANGO_SECRET = os.getenv('DJANGO_SECRET')
DJANGO_DEBUG = bool(strtobool(os.getenv('DJANGO_DEBUG')))
DJANGO_CSRF_TRUSTED_ORIGINS = ast.literal_eval(os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS'))
DJANGO_ALLOWED_HOSTS = ast.literal_eval(os.getenv('DJANGO_ALLOWED_HOSTS'))

DJANGO_CORS_ALLOWED_ORIGINS = ast.literal_eval(os.getenv('DJANGO_CORS_ALLOWED_ORIGINS'))

DJANGO_MINIO_STORAGE_ENDPOINT = os.getenv('DJANGO_MINIO_STORAGE_ENDPOINT')
DJANGO_MINIO_STORAGE_ACCESS_KEY = os.getenv('DJANGO_MINIO_STORAGE_ACCESS_KEY')
DJANGO_MINIO_STORAGE_SECRET_KEY = os.getenv('DJANGO_MINIO_STORAGE_SECRET_KEY')
DJANGO_MINIO_STORAGE_USE_HTTPS = bool(strtobool(os.getenv('DJANGO_MINIO_STORAGE_USE_HTTPS')))
DJANGO_MINIO_STORAGE_MEDIA_BUCKET_NAME = os.getenv('DJANGO_MINIO_STORAGE_MEDIA_BUCKET_NAME')
DJANGO_MINIO_STORAGE_STATIC_BUCKET_NAME = os.getenv('DJANGO_MINIO_STORAGE_STATIC_BUCKET_NAME')
DJANGO_MINIO_STORAGE_MEDIA_URL = os.getenv('DJANGO_MINIO_STORAGE_MEDIA_URL')
DJANGO_MINIO_STORAGE_STATIC_URL = os.getenv('DJANGO_MINIO_STORAGE_STATIC_URL')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DJANGO_DEBUG

ALLOWED_HOSTS = DJANGO_ALLOWED_HOSTS

CSRF_TRUSTED_ORIGINS = DJANGO_CSRF_TRUSTED_ORIGINS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party apps
    'django_prometheus',
    'minio_storage',
    'corsheaders',
    'rest_framework',
    'drf_yasg',

    # project apps
    'createdatabase',
    'createsuperuser',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.parent / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# https://docs.djangoproject.com/en/4.1/topics/cache/#redis
CACHES = {
    'default': {
        'BACKEND': 'django_prometheus.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_USER}:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}',
    }
}

# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
}

if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        "rest_framework.renderers.BrowsableAPIRenderer")


# https://pypi.org/project/django-cors-headers/
# For demo purposes only. Use a white list in the real world.
CORS_ALLOWED_ORIGINS = DJANGO_CORS_ALLOWED_ORIGINS


# https://django-minio-storage.readthedocs.io/en/latest/
DEFAULT_FILE_STORAGE = 'minio_storage.storage.MinioMediaStorage'
STATICFILES_STORAGE = 'minio_storage.storage.MinioStaticStorage'
MINIO_STORAGE_ENDPOINT = DJANGO_MINIO_STORAGE_ENDPOINT
MINIO_STORAGE_ACCESS_KEY = DJANGO_MINIO_STORAGE_ACCESS_KEY
MINIO_STORAGE_SECRET_KEY = DJANGO_MINIO_STORAGE_SECRET_KEY
MINIO_STORAGE_USE_HTTPS = DJANGO_MINIO_STORAGE_USE_HTTPS
MINIO_STORAGE_MEDIA_BUCKET_NAME = DJANGO_MINIO_STORAGE_MEDIA_BUCKET_NAME
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_STATIC_BUCKET_NAME = DJANGO_MINIO_STORAGE_STATIC_BUCKET_NAME
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
MINIO_STORAGE_MEDIA_URL = DJANGO_MINIO_STORAGE_MEDIA_URL
MINIO_STORAGE_STATIC_URL = DJANGO_MINIO_STORAGE_STATIC_URL


# https://github.com/korfuri/django-prometheus
PROMETHEUS_EXPORT_MIGRATIONS = True
