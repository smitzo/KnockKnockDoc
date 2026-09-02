#!/bin/sh
set -eu

python manage.py migrate --noinput
python manage.py ensure_demo_admin

exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-2}" \
  --threads "${GUNICORN_THREADS:-4}" \
  --timeout 30 \
  --access-logfile - \
  --error-logfile -
