#!/usr/bin/env bash
service nginx start
uwsgi --ini uwsgi.ini
cd ..
celery -A celery_app.celery worker --loglevel=info