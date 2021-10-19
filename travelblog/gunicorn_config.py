import os

import decouple

command = os.path.join(decouple.config('VENV_DIR'), 'bin', 'gunicorn')
pythonpath = decouple.config('PROJECT_DIR')
bind = '127.0.0.1:8001'
workers = 3
user = decouple.config('USER')
raw_env = 'DJANGO_SETTINGS_MODULE=travelblog.settings'
