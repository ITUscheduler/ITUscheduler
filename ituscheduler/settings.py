import json
import os

import sentry_sdk
from kombu.utils.url import safequote
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

SECRET_KEY = os.environ.get('ITUSCHEDULER_SECRET_KEY', 'notsosecretkey')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.environ.get('ITUSCHEDULER_STAGE', 'development') == 'development'
ADMINS = [('Doruk', 'doruk@gezici.me')]

ALLOWED_HOSTS = ['.ituscheduler.com', '.localhost', '127.0.0.1', '::1']
CSRF_TRUSTED_ORIGINS = ['https://ituscheduler.com']

if os.getenv('ECS_CONTAINER_METADATA_FILE'):
    metadata_file_path = os.environ['ECS_CONTAINER_METADATA_FILE']

    with open(metadata_file_path) as f:
        metadata = json.load(f)

    private_ip = metadata["HostPrivateIPv4Address"]
    ALLOWED_HOSTS.append(private_ip)
    CSRF_TRUSTED_ORIGINS.append(f'http://{private_ip}')

# Reverse Proxy
if not DEBUG:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

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
    'font_awesome',
    'django_celery_results',
    'django_celery_beat',
    'celery_progress',
    # apps
    'ituscheduler.api',
    'ituscheduler.scheduler',
    'ituscheduler.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
                'ituscheduler.scheduler.context_processors.global_processor',
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

AUTH_USER_MODEL = 'scheduler.ExtendedUser'

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

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

SITE_ID = 1
MIGRATION_MODULES = {
    'sites': 'ituscheduler.migrations',
}

# Email
EMAIL_HOST = os.environ.get('ITUSCHEDULER_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('ITUSCHEDULER_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('ITUSCHEDULER_EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
EMAIL_PORT = 465
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Social Auth
SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIAL_AUTH_TWITTER_KEY = os.environ.get('ITUSCHEDULER_SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('ITUSCHEDULER_SOCIAL_AUTH_TWITTER_SECRET')

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('ITUSCHEDULER_SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('ITUSCHEDULER_SOCIAL_AUTH_FACEBOOK_SECRET')

# AWS
AWS_ACCESS_KEY_ID = safequote(str(os.environ.get('ITUSCHEDULER_AWS_ACCESS_KEY_ID')))
AWS_SECRET_ACCESS_KEY = safequote(str(os.environ.get('ITUSCHEDULER_AWS_SECRET_ACCESS_KEY')))
AWS_DEFAULT_REGION = os.environ.get('ITUSCHEDULER_AWS_DEFAULT_REGION')

# Sentry
sentry_sdk.init(
    dsn=os.environ.get('ITUSCHEDULER_SENTRY_DSN'),
    environment=os.environ.get('ITUSCHEDULER_STAGE', 'development'),
    integrations=[DjangoIntegration(), CeleryIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.1,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
