import datetime
import os

from decouple import config
from django.template.loader import render_to_string
from django.core.signing import Signer

from travelblog import settings

signer = Signer()


def get_timestamp_path(instance, filename):
    return f'{datetime.datetime.now().timestamp()}{os.path.splitext(filename)[1]}'


def send_activation_notification(user):
    host = 'http://localhost:8000'
    if not settings.DEBUG:
        host = 'http://' + settings.HOST

    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text, config('MAIL_USER'))


def send_new_comment_notification(comment):
    host = 'http://localhost:8000'
    if not settings.DEBUG:
        host = 'http://' + settings.HOST

    author = comment.article.author
    context = {
        'author': author,
        'host': host,
        'comment': comment,
    }
    subject = render_to_string('email/new_comment_letter_subject.txt', context)
    body_text = render_to_string('email/new_comment_letter_body.txt', context)
    author.email_user(subject, body_text, config('MAIL_USER'))
