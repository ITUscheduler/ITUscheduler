import os

from django.conf import settings

broker_url = f'sqs://{settings.AWS_ACCESS_KEY_ID}:{settings.AWS_SECRET_ACCESS_KEY}@'
broker_transport_options = {
    'region': settings.AWS_DEFAULT_REGION,
    'queue_name_prefix': f"ituscheduler-{os.environ.get('ITUSCHEDULER_STAGE', 'development')}-",
}
result_backend = 'django-db'
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

timezone = settings.TIME_ZONE

task_track_started = True
task_publish_retry = False
