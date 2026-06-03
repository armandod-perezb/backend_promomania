#!/bin/sh
set -e

echo "Aplicando collectstatic..."
python manage.py collectstatic --noinput

echo "Aplicando migraciones..."
python manage.py migrate

echo "Creando usuario admin de Django..."
python manage.py create_admin

echo "Iniciando Gunicorn..."
gunicorn backprom.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers ${WEB_CONCURRENCY:-2} \
  --timeout 120
