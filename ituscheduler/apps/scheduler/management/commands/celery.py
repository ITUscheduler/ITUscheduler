from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'Runs celery beat worker'

    def handle(self, *args, **options):
        subprocess.call(["celery", "-A", "ituscheduler", "worker", "-B", "-l", "info", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"])
