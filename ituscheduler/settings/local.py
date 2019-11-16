from .base import *
from .secrets import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('ITUSCHEDULER_POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('ITUSCHEDULER_POSTGRES_PORT', '5432'),
        'USER': os.environ.get('ITUSCHEDULER_POSTGRES_USER', 'ituscheduler'),
        'PASSWORD': os.environ.get('ITUSCHEDULER_POSTGRES_PASSWORD', 'ituscheduler'),
        'NAME': os.environ.get('ITUSCHEDULER_POSTGRES_DATABASE', 'ituscheduler'),
    }, 'rds': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_NAME,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': '5432',
    }
}
