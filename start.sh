#!/usr/bin/env sh
set -e
pip install --upgrade pip
python manage.py collectstatic --clear --no-input -v 0
#python manage.py runserver "${WEB_HOST}":"${WEB_PORT}"
python manage.py migrate
#export DJANGO_SETTINGS_MODULE="short_link_service.settings"
exec gunicorn --bind "${WEB_HOST}":"${WEB_PORT}"  --workers "${APP_WORKERS}" link_app.wsgi