#!/bin/bash
source /home/gii/django_travelblog/venv/bin/activate
exec gunicorn -c "/home/gii/django_travelblog/travelblog/gunicorn_config.py" travelblog.wsgi
