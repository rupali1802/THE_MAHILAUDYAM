"""
Django settings for development using MySQL.
Usage: python manage.py runserver --settings=mahila_udyam_backend.settings_dev
"""
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mahila_udyam',
        'USER': 'root',
        'PASSWORD': 'prathap@0210',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

DEBUG = True
print("✅ Using MySQL (development mode) - User: root")
