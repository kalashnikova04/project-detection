#!/usr/bin/env bash

set -e

echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py createsuperuser_if_none_exists \
        --user $DJANGO_SUPERUSER_USERNAME \
        --password $DJANGO_SUPERUSER_PASSWORD \
        --email $DJANGO_SUPERUSER_EMAIL
# python manage.py clear_tasks


exec "$@"
