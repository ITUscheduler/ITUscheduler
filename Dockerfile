FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /ituscheduler

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY manage.py manage.py
COPY fixtures fixtures
COPY ituscheduler ituscheduler

RUN python manage.py collectstatic --no-input

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

CMD ["docker-entrypoint.sh"]
