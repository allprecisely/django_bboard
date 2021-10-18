command = '/usr/local/bin/gunicorn'
pythonpath = '/usr/src/app/travelblog'
bind = '0.0.0.0:8001'
workers = 3
raw_env = 'DJANGO_SETTINGS_MODULE=travelblog.settings'
