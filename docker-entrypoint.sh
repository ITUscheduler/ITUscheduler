#!/bin/bash
set -eo pipefail

PROJECT=ituscheduler

if [[ "$ITUSCHEDULER_STAGE" == "local" ]]; then
    export DJANGO_SETTINGS_MODULE="$PROJECT".settings.local
else
    export DJANGO_SETTINGS_MODULE="$PROJECT".settings.production
fi

case "$CONTAINER_KIND" in
    web)
        if [[ "$ITUSCHEDULER_STAGE" == "local" ]]; then
            exec python manage.py runserver 0.0.0.0:8000
        else
            exec gunicorn "$PROJECT".wsgi:application \
                --bind=0.0.0.0:80 \
                --log-level=info \
                --log-file=-
        fi
    ;;
    celery)
        exec python manage.py celery
    ;;
    *)
        echo >&2 "Invalid CONTAINER_KIND: $CONTAINER_KIND."
        exit 1
esac
