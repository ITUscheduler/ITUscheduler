from .base import *

DEBUG = False

from .secrets import SOCIAL_AUTH_FACEBOOK_KEY, SOCIAL_AUTH_FACEBOOK_SECRET, SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET
from .secrets import POSTGRES_NAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES_NAME,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': '',
    }, 'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
