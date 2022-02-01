#!/bin/bash
set -eo pipefail

PROJECT=ituscheduler

# run validation script
python3 scripts/startup_check.py

case "$ITUSCHEDULER_CONTAINER_KIND" in
    web)
        if [[ "$ITUSCHEDULER_STAGE" == "development" ]]; then
            exec python manage.py runserver 0.0.0.0:8000
        else
            python manage.py migrate
            exec gunicorn "$PROJECT".wsgi:application --workers 2 --bind=0.0.0.0:80
        fi
    ;;
    worker)
        exec celery --app "$PROJECT" worker --concurrency 20 -l INFO
    ;;
    beat)
        exec celery --app "$PROJECT" beat -l INFO
    ;;
    *)
        echo >&2 "Invalid ITUSCHEDULER_CONTAINER_KIND: $ITUSCHEDULER_CONTAINER_KIND."
        exit 1
esac
