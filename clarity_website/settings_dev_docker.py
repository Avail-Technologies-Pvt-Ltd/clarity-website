# settings_dev_docker.py — clarity_website
# Development inside Docker (uses PostgreSQL from docker-compose.dev.yml)
from .settings import *
from decouple import config

DEBUG = True
SECRET_KEY = config('SECRET_KEY', default='dev-insecure-key-docker')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='db'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
