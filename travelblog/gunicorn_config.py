import os

from decouple import config

command = os.path.join(config('VENV_DIR'), 'bin', 'gunicorn')
pythonpath = config('PROJECT_DIR')
bind = '127.0.0.1:8001'
workers = 3
user = config('USER')
raw_env = 'DJANGO_SETTINGS_MODULE=travelblog.settings'
