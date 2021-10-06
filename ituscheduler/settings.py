import os

import sentry_sdk
from kombu.utils.url import safequote
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

SECRET_KEY = os.environ.get('SECRET_KEY', 'on+@th%h49ncw2+v%i*8cgz8)6_@koy1j1rd7cq@s@=8y6(6%8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not os.environ.get('ITUSCHEDULER_STAGE') == 'development':
    SOCIAL_AUTH_POSTGRES_JSONFIELD = True
    SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
else:
    DEBUG = True

ADMINS = [('Doruk', 'doruk@gezici.me')]
ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'rest_framework',
    'bootstrapform',
    'django_gravatar',
    'social_django',
    'meta',
    'font_awesome',
    'django_celery_results',
    'django_celery_beat',
    'celery_progress',
    'debug_toolbar',
    # apps
    'ituscheduler.apps.api',
    'ituscheduler.apps.scheduler',
    'ituscheduler.apps.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware'
]

ROOT_URLCONF = 'ituscheduler.urls'

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
                'ituscheduler.apps.scheduler.context_processors.global_processor',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'ituscheduler.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('ITUSCHEDULER_POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('ITUSCHEDULER_POSTGRES_PORT', '5432'),
        'USER': os.environ.get('ITUSCHEDULER_POSTGRES_USER', 'ituscheduler'),
        'PASSWORD': os.environ.get('ITUSCHEDULER_POSTGRES_PASSWORD', 'ituscheduler'),
        'NAME': os.environ.get('ITUSCHEDULER_POSTGRES_NAME', 'ituscheduler'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "scheduler.ExtendedUser"
SOCIAL_AUTH_USER_MODEL = "scheduler.ExtendedUser"

AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

SITE_ID = 1
MIGRATION_MODULES = {
    'sites': 'ituscheduler.migrations',
}

META_SITE_PROTOCOL = 'https'
META_USE_SITES = True

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
EMAIL_PORT = 465
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SOCIAL_AUTH_TWITTER_KEY = os.environ.get('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('SOCIAL_AUTH_TWITTER_SECRET')

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')

AWS_ACCESS_KEY_ID = safequote(str(os.environ.get('AWS_ACCESS_KEY_ID')))
AWS_SECRET_ACCESS_KEY = safequote(str(os.environ.get('AWS_SECRET_ACCESS_KEY')))

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = "sqs://{aws_access_key}:{aws_secret_key}@".format(
    aws_access_key=AWS_ACCESS_KEY_ID, aws_secret_key=AWS_SECRET_ACCESS_KEY,
)
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'eu-west-1'
}
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Sentry
sentry_sdk.init(
    dsn=os.environ.get('ITUSCHEDULER_SENTRY_DSN'),
    environment=os.environ.get('ITUSCHEDULER_STAGE', 'development'),
    integrations=[DjangoIntegration(), CeleryIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
