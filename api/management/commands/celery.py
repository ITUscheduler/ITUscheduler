from django.core.management.base import BaseCommand
import subprocess
import os


class Command(BaseCommand):
    help = 'Runs celery beat worker'

    def handle(self, *args, **options):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITUscheduler.settings.local')
        subprocess.call(["celery", "-A", "ITUscheduler", "beat", "-l", "info", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"])
