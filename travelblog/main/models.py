from django.db import models
from django.contrib.auth.models import AbstractUser

from main import utilities


class TravelUser(AbstractUser):
    is_activated = models.BooleanField(
        default=True, db_index=True, verbose_name='Прошел активацию?'
    )
    send_messages = models.BooleanField(
        default=True, verbose_name='Слать оповещения о новых комментариях?'
    )

    def delete(self, *args, **kwargs):
        for article in self.article_set.all():
            article.delete()
        super().delete(*args, **kwargs)


class AdditionalImage(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name='Статья')
    image = models.ImageField(
        upload_to=utilities.get_timestamp_path, verbose_name='Изображение'
    )

    class Meta:
        verbose_name_plural = 'Дополнительные изображения'
        verbose_name = 'Дополнительное изображение'


class Article(models.Model):
    city = models.ForeignKey(
        'City', on_delete=models.PROTECT, verbose_name='Город'
    )
    title = models.CharField(max_length=40, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(
        blank=True, upload_to=utilities.get_timestamp_path, verbose_name='Изображение'
    )
    author = models.ForeignKey(
        TravelUser, on_delete=models.CASCADE, verbose_name='Автор статьи'
    )
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='Выводить в списке?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Опубликовано'
    )

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Статьи'
        verbose_name = 'Статья'
        ordering = ['-created_at']


class Place(models.Model):
    name = models.CharField(
        max_length=20, db_index=True, unique=True, verbose_name='Название'
    )
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    country = models.ForeignKey(
        'Country',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Страна',
    )


class CountryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(country__isnull=True)


class Country(Place):
    objects = CountryManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class CityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(country__isnull=False)


class City(Place):
    objects = CityManager()

    def __str__(self):
        return f'{self.country.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('country__order', 'country__name', 'order', 'name')
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='Выводить на экран?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Опубликован'
    )

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].article.author
    if kwargs['created'] and author.send_messages:
        utilities.send_new_comment_notification(kwargs['instance'])


models.signals.post_save.connect(post_save_dispatcher, sender=Comment)
