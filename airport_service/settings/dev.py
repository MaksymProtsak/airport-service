from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
import os
DEBUG = os.environ.get("DJANGO_DEBUG", "") != 'False'

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}