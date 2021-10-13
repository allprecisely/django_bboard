import random
import string

from celery import shared_task

from main import models


@shared_task
def create_new_bb():
    rubrics = models.SubRubric.objects.all()
    rand_rubric = random.choice(rubrics)
    authors = models.AdvUser.objects.all()
    rand_author = random.choice(authors)
    formed_name = (
        rand_rubric.name
        + '_'
        + ''.join(random.choices(string.ascii_letters, k=5))
    )
    new_object = models.Bb.objects.create(
        rubric=rand_rubric,
        title=formed_name,
        content=''.join(random.choices(string.ascii_letters, k=20)),
        price=random.random(),
        contacts=''.join(random.choices(string.ascii_letters, k=5)),
        author=rand_author,
    )
    return new_object.title
