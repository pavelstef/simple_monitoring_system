#!/bin/bash
source /home/<project_folder>/sms/venv/bin/activate
exec flower -A sms --port=5555
