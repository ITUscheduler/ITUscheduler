import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ituscheduler.settings')

app = Celery('ituscheduler')
app.config_from_object('ituscheduler.celery_config')
app.autodiscover_tasks()
