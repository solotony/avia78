from django.db import models
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.fields import ThumbnailerImageField
from time import strftime
from random import randint
from django.utils.html import mark_safe
import os
from django.urls import reverse
from datetime import datetime
from urllib.parse import urljoin

class GalleryCategory(models.Model):

    ORIENT_SQUARE = 'S'
    ORIENT_PORTRAIT = 'P'
    ORIENT_ALBUM = 'A'
    ORIENT_ANY = 'N'
    ORIENT_CHOICES = (
        (ORIENT_SQUARE, 'Смешенная ониентация - квадратные превьюшки'),
        (ORIENT_PORTRAIT, 'Портретная ониентация - вертикальные превьюшки'),
        (ORIENT_ALBUM, 'Альбомная ориентация - горизонтальные превьюшки'),
        (ORIENT_ANY, 'Смешенная ониентация - произвольные превьюшки'),
    )

    orient = models.CharField(
        max_length=1,
        choices=ORIENT_CHOICES,
        default=ORIENT_SQUARE,
    )

    name = models.CharField(
        null=False,
        blank=False,
        max_length=100,
        verbose_name='название категории',
        help_text='не более 100 символов, используется для манипуляции с категорией, а также по умолчанию в качестве title, description, header')

    slug = models.SlugField(
        max_length=200,
        null=False,
        blank=False,
        unique=True,
        verbose_name='уникальный адрес страницы',
    )

    title = models.CharField(
        null=True,
        blank=True,
        max_length=300,
        verbose_name='поле title новости',
        help_text='не более 300 символов, по умолчанию будет использовано "название категории" (если не знаете что это такое - спросите у своего SEO-шника)'
    )

    description = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='поле description новости',
        help_text='не более 500 символов, по умолчанию будет использован "краткий текст", а при его отсутствии - "название категории"  (если не знаете что это такое - спросите у своего SEO-шника)'
    )

    header = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='основной заголовок новости',
        help_text='не более 200 символов, по умолчанию будет использовано "название категории"'
    )

    abstract = models.TextField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='краткий текст на страницу',
        help_text='не более 500 символов '
    )

    def __str__(self):
        return self.name

    def get_title(self):
        if (self.title):
            return self.title
        return self.name

    def get_description(self):
        if (self.description):
            return self.description
        if (self.abstract):
            return self.abstract
        return self.name

    def get_header(self):
        if (self.header):
            return self.header
        return self.name

    def get_url(self):
        if (self.slug):
            return reverse('gallery.category_by_slug', args=(self.slug,))
        return reverse('gallery.category', args=(self.id,))

    def tn_width(self):
        if (self.orient == GalleryCategory.ORIENT_SQUARE):
            return 270
        elif (self.orient == GalleryCategory.ORIENT_PORTRAIT):
            return 270
        else: #(self.orient == GalleryCategory.ORIENT_ALBUM):
            return 370

    def tn_height(self):
        if (self.orient == GalleryCategory.ORIENT_SQUARE):
            return 270
        elif (self.orient == GalleryCategory.ORIENT_PORTRAIT):
            return 370
        else: #(self.orient == GalleryCategory.ORIENT_ALBUM):
            return 270

    def get_image(self):
        return self.entries.first()

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'
        ordering = ('name',)

    @staticmethod
    def get_sitemap_info(domain):
        return {
            'name': 'gallery.xml',
            'loc':  urljoin(domain, 'sitemap/gallery.xml'),
            'lastmod': datetime.now().isoformat()
        }

    @staticmethod
    def get_sitemap(domain, priority):
        sitemap = [{
            'loc': urljoin(domain, reverse('gallery.categories')),
            'lastmod': datetime.now().isoformat(),
            'priority':priority
        }]
        for url in GalleryCategory.objects.all():
            sitemap.append({
                'loc':urljoin(domain, url.get_url()),
                'lastmod': datetime.now().isoformat(),
                'priority':priority*0.8
            })
        return sitemap

    def get_photos_all(self):
        return self.entries.all()


class Photo(models.Model):

    category = models.ForeignKey(
        GalleryCategory,
        null=False,
        blank=False,
        verbose_name='категория',
        on_delete=models.CASCADE,
        related_name='entries'
    )

    name = models.CharField(
        null=False,
        blank=True,
        max_length=200,
        verbose_name='подпись изображения',
        help_text='не более 200 символов'
    )

    def get_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return os.path.join(
            "media/gallery/", strftime("%Y/%m/%d/"), str(randint(10000000, 99999999)) + file_extension)

    image = ThumbnailerImageField(
        null=True,
        blank=True,
        verbose_name='Основное изображение новости',
        help_text='размеры изображения на странице новости -  770x562 (обрезается), '
                  'в списке новостей - 370x270 (обрезается)',
        upload_to=get_upload_path,
    )

    sort_order = models.IntegerField(
        null=False,
        blank=False,
        default = 0,
        verbose_name='порядок'
    )

    def image_tag(self):
        if (self.image):
            thumb_url = get_thumbnailer(self.image.name)['admin'].url
            return  mark_safe('<img src="%s" />' % thumb_url)
        return None

    image_tag.short_description = 'Превью'
    image_tag.allow_tags = True

    def image_thumb_url(self):
        if (self.image):
            return get_thumbnailer(self.image.name)['gallery.thumb'].url
        return None

    def image_full_url(self):
        if (self.image):
            return get_thumbnailer(self.image.name)['gallery.full'].url
        return None

    def image_front_url(self):
        if (self.image):
            return get_thumbnailer(self.image.name)['gallery.front'].url
        return None

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображение'
        ordering = ('sort_order',)
