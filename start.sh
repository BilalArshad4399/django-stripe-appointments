#!/bin/bash
echo "Starting Sofia Health application..."
echo "Running database migrations..."
python manage.py migrate --noinput
echo "Migrations completed."
echo "Starting Gunicorn server..."
exec gunicorn sofia_health.wsgi --bind 0.0.0.0:${PORT:-8000}