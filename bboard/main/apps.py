from django.apps import AppConfig
from django.dispatch import Signal

from .utilities import send_activation_notification

user_register = Signal(providing_args=['instance'])


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'Miles of Life'


def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_register.connect(user_registered_dispatcher)
