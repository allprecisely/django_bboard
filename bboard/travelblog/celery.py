import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelblog.settings')

app = Celery('travelblog')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'creating-new-objects': {
        'task': 'main.tasks.create_new_article',
        'schedule': 10,
    }
}
