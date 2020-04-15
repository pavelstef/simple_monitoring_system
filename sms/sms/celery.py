""" Celery base configuration """


import os
from celery import Celery
from celery.schedules import crontab


CELERY_LOOP_TIME = 5

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms.settings')

celery_app = Celery('sms')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

# celery beat tasks
celery_app.conf.beat_schedule = {
    'device_check_loop': {
        'task': 'sms_core.tasks.task_device_check_loop',
        'schedule': crontab(minute=f'*/{CELERY_LOOP_TIME}'),
    },
}
