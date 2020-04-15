#!/bin/bash
source /home/<project_folder>/sms/venv/bin/activate
exec celery -A sms worker -l info
