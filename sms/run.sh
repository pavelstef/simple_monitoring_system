#!/bin/bash

echo '=== Waiting for DB ==='
sleep 5

echo '=== Preparing DB ==='
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py inituser

#echo '=== Run Celery ==='
#exec celery -A sms worker -l info --logfile=./logs/celery.log -B -n celery

#echo '=== Waiting for Celery ==='
#sleep 2

#echo '=== Run Flower ==='
#exec flower -A sms --port=5555

echo '=== Run APP ==='
exec gunicorn --bind=0.0.0.0:8001 --workers=4 sms.wsgi
