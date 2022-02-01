FROM python:3.10

ENV PYTHONUNBUFFERED 1
WORKDIR /ituscheduler

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ituscheduler ituscheduler
COPY fixtures fixtures
COPY scripts scripts
COPY manage.py manage.py

RUN python manage.py collectstatic --no-input

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

CMD ["docker-entrypoint.sh"]
