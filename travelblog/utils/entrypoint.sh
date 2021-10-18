#!/bin/bash

python3 manage.py makemigrations --no-input

python3 manage.py migrate --no-input

exec gunicorn -c "${PROJECT_DIR}/gunicorn_config.py" travelblog.wsgi