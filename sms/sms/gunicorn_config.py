""" Gunicorn config """

command = '/home/<project_folder>/sms/venv/bin/gunicorn'
pythonpath = '/home/<project_folder>/sms/'
bind = '127.0.0.1:8001'
workers = 3
user = <your_user>
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=sms.settings'
