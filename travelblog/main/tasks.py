import random
import string

from celery import shared_task

from main import models


@shared_task
def create_new_article():
    cities = models.City.objects.all()
    rand_city = random.choice(cities)
    authors = models.TravelUser.objects.all()
    rand_author = random.choice(authors)
    formed_name = (
        rand_city.name
        + '_'
        + ''.join(random.choices(string.ascii_letters, k=5))
    )
    new_object = models.Article.objects.create(
        city=rand_city,
        title=formed_name,
        content=''.join(random.choices(string.ascii_letters, k=20)),
        author=rand_author,
    )
    return new_object.title
