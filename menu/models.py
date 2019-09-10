from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

# Create your models here.

class FixedPage(models.Model):

    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name='наименование страницы',
    )

    link = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='адрес страницы'
    )

    def get_url(self, mode=None):
        return self.link

    class Meta:
        verbose_name = 'Фиксированная страница'
        verbose_name_plural = 'Фиксированные страницы'

    def __str__(self):
        return self.name + ' (' + self.link + ')'

class MenuItem(MPTTModel):

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name='Родитель',
        on_delete=models.DO_NOTHING,
        db_index = True,
        related_name='children'
    )

    title = models.CharField(
        max_length=128,
        null=False,
        blank=True,
        verbose_name='текст в меню',
    )

    link = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='произвольная ссылка'
    )

    def __str__(self):
        return self.title + ' (' + self.get_url() + ')'

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def get_url(self):
        if self.link:
            return self.link
        if self.content_object:
            return self.content_object.get_url()
        return ''

    def get_text(self):
        return self.title

    def get_childs(self):
        return self.get_children()

    limit = \
        models.Q(app_label='menu', model='FixedPage') | \
        models.Q(app_label='pages', model='Page')

    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limit,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='тип содержимого',
    )

    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    content_object = fields.GenericForeignKey('content_type', 'object_id')

