command = '/home/gii/django_travelblog/venv/bin/gunicorn'
pythonpath = '/home/gii/django_travelblog/travelblog'
bind = '127.0.0.1:8001'
workers = 3
user = 'gii'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=travelblog.settings'
