#!/bin/bash
set -eo pipefail

PROJECT=ituscheduler

case "$CONTAINER_KIND" in
    web)
        if [[ "$ITUSCHEDULER_STAGE" == "development" ]]; then
            exec python manage.py runserver 0.0.0.0:8000
        else
            exec gunicorn "$PROJECT".wsgi:application \
                --bind=0.0.0.0:80 \
                --log-level=info \
                --log-file=-
        fi
    ;;
    worker)
        exec celery --app ituscheduler worker --concurrency 20 -l INFO
    ;;
    beat)
        exec celery --app ituscheduler beat --scheduler django_celery_beat.schedulers:DatabaseScheduler -l INFO
    ;;
    *)
        echo >&2 "Invalid CONTAINER_KIND: $CONTAINER_KIND."
        exit 1
esac
