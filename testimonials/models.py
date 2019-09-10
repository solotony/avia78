from django.db import models
from random import randint
from time import strftime
import os
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
from django.utils.html import mark_safe
from django.urls import reverse
from common.models import get_upload_path
from urllib.parse import urljoin
import datetime

class Testimonial(models.Model):

    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Имя',
        help_text='не более 100 символов')

    text = models.TextField(
        max_length=5000,
        null=True,
        blank=True,
        verbose_name='Текст',
        help_text='не более 5000 символов')

    moderated = models.BooleanField(
        default=False,
        verbose_name='Отзыв проверен',
    )

    created_at = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата отзыва',
        #auto_now_add = True,
        #editable=True
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return 'Отзыв ' + str(self.id)

    def get_upload_path(instance, filename):
        return get_upload_path('tstmnl', filename)

    image = ThumbnailerImageField(
        null=True,
        blank=True,
        verbose_name='Фотография для отзыва',
        upload_to=get_upload_path,
        help_text=''
    )

    def image_tag(self):
        thumb_url = get_thumbnailer(self.image.name)['admin'].url
        return  mark_safe('<img src="%s" />' % thumb_url)

    image_tag.short_description = 'Превью'
    image_tag.allow_tags = True

    scan = ThumbnailerImageField(
        null=True,
        blank=True,
        verbose_name='Скан отзыва',
        upload_to=get_upload_path,
        help_text=''
    )

    def scan_tag(self, mode=None):
        thumb_url = get_thumbnailer(self.scan.name)['admin'].url
        return mark_safe('<img src="%s" />' % thumb_url)

    scan_tag.short_description = 'Превью'
    scan_tag.allow_tags = True

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def image_thumb_url(self):
        return get_thumbnailer(self.image)['testimonial.person'].url

    def scan_thumb_url(self):
        return get_thumbnailer(self.scan)['testimonial.scan.tn'].url

    def scan_url(self):
        return get_thumbnailer(self.scan)['testimonial.scan'].url

    def get_url(self, mode=None):
        return reverse('testimonials.show', args=(self.id,))

    @staticmethod
    def get_front_all():
        return Testimonial.objects.filter(text__isnull=False).exclude(text='').order_by('-created_at').all()[:10]

    @staticmethod
    def get_admin_edit_all():
        r = str(randint(10000000,99999999))
        return mark_safe('<a href="/admin/testimonials/testimonial/" style="background-color: #000;color:#CC0000; padding:6px;">редактировать</a> ' \
               '<script id="rand'+r+'">document.getElementById("rand'+r+'").parentNode.style.border = "4px dashed #CC0000";</script>')

    def get_admin_edit(self):
        r = str(randint(10000000,99999999))
        return mark_safe('<a href="/admin/testimonials/testimonial/'+str(self.id)+'/change/" style="background-color: #000;color:#CC0000; padding:6px;">редактировать</a> '
                '<script id="rand' + r + '">document.getElementById("rand' + r + '").parentNode.style.border = "4px dashed #CC0000";</script>')

    def get_breadcrumbs(self, terminate=True):
        return '<li><a href="' + reverse('testimonials.list') +'">Отзывы</a></li><li>' + self.get_title() + '</li>'

    def get_title(self):
        return self.__str__()

    def get_description(self):
        if self.text:
            return self.text[:250]
        return self.__str__()

    @staticmethod
    def get_sitemap_info(domain):
        return {
            'name': 'testimonial.xml',
            'loc': urljoin(domain, 'sitemap/testimonial.xml'),
            'lastmod': datetime.datetime.now().isoformat()
        }

    @staticmethod
    def get_sitemap(domain, priority):
        sitemap = []
        for url in Testimonial.objects.all():
            date = url.created_at if url.created_at else datetime.datetime.now()

            sitemap.append({
                'loc': urljoin(domain, url.get_url()),
                'lastmod': date.isoformat(),
                'priority': priority
            })
        return sitemap