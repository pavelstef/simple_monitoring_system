#!/bin/bash
source /home/<project_folder>/sms/venv/bin/activate
exec gunicorn  -c "/home/<project_folder>/sms/sms/gunicorn_config.py" sms.wsgi
