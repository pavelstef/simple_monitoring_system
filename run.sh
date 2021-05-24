#!/bin/bash

echo '=== Waiting for DB ==='
sleep 2

echo '=== Preparing DB ==='
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py inituser

echo '=== Preparing Static files ==='
python manage.py collectstatic --noinput

echo '=== Run APP ==='
exec gunicorn --bind=0.0.0.0:8001 --workers=4 sms.wsgi
