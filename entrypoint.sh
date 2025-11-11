#!/bin/sh

set -e

echo "Running database migrations..."
python manage.py migrate --noinput --settings=config.settings.prod

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings.prod

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
