from django.db import models
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.fields import ThumbnailerImageField
import os
from time import strftime
from random import randint
from django.utils.html import mark_safe
from django.urls import reverse
from django.db.models import Q, Count
from django.utils import timezone
import datetime
from urllib.parse import urljoin
import csv
from django.db import connection

class Post(models.Model):

    slug = models.SlugField(
        max_length=200,
        null=False,
        blank=False,
        unique=True,
        verbose_name='уникальный адрес страницы',
    )

    name = models.CharField(
        null=False,
        blank=False,
        max_length=300,
        verbose_name='заголовок',
        help_text='не более 300 символов, используется для манипуляции с новостью, а также по умолчанию в качестве title, description, header')

    title = models.CharField(
        null=True,
        blank=True,
        max_length=300,
        verbose_name='поле title',
        help_text='не более 300 символов, по умолчанию будет использовано "название" (если не знаете что это такое - спросите у своего SEO-шника)'
    )

    description = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='поле description',
        help_text='не более 500 символов, по умолчанию будет использован "анонс", а при его отсутствии - "название"  (если не знаете что это такое - спросите у своего SEO-шника)'
    )

    header = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='основной заголовок',
        help_text='не более 200 символов, по умолчанию будет использовано "заголовок"'
    )

    abstract = models.TextField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='анонс',
        help_text='не более 500 символов, по умолчанию будут использованы первые ч00 знаков "текста". анонс не выводится на странице с текстом'
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='текст',
        help_text = 'если это поле пустое, то прикрепленное изображение выводится по центру на всю страницу'
    )

    search_data = models.CharField(
        null=True,
        blank=True,
        max_length=10000,
        verbose_name='данные для поиска',
    )

    published_at = models.DateField(
        null=False,
        blank=False,
        verbose_name='дата публикации',
        default=datetime.date.today,
    )

    valid_from = models.DateField(
        null=True,
        blank=True,
        verbose_name='с',
        help_text='дата, начиная с которой включительно новость отображается'
    )

    valid_to = models.DateField(
        null=True,
        blank=True,
        verbose_name='до',
        help_text='дата, до которой включительно новость отображается'
    )

    def get_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return os.path.join(
            "media/newsimages/", strftime("%Y/%m/%d/"), str(randint(10000000, 99999999)) + file_extension)

    image = ThumbnailerImageField(
        null=True,
        blank=True,
        verbose_name='Основное изображение',
        help_text='размеры изображения на странице -  770x562 (обрезается), '
                  'в списке - 370x270 (обрезается)',
        upload_to=get_upload_path,
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
            return get_thumbnailer(self.image.name)['news.thumb'].url
        return None

    def image_full_url(self):
        if (self.image):
            return get_thumbnailer(self.image.name)['news.full'].url
        return None

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

    def get_year(self):
        return self.published_at.year

    def get_month(self):
        return self.published_at.month

    def get_abstract(self):
        if (self.abstract):
            return self.abstract
        return self.content[:200-len(self.get_header())]

    def get_date_str(self):
        return self.published_at.strftime('%d.%m.%Y')

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'
        ordering = ('-published_at',)

    def get_url(self):
        if (self.slug):
            return reverse('news.post_detail_canonical', args=(self.slug,))
        return ''

    def get_url_html(self):
        if (self.slug):
            return reverse('news.post_detail_html', args=(self.get_year(),self.get_month(),self.slug,))
        return ''

    def get_canonical(self):
        return self.get_url_html()

    get_url.short_description = 'qqq'
    get_url.allow_tags = True

    def save(self, *args, **kwargs):
        self.search_data = self.name + ' ' + self.content
        self.search_data = self.search_data [:10000]
        super(Post, self).save(*args, **kwargs)


    @staticmethod
    def list_objects():
        return Post.objects.order_by('-published_at').all()

    @staticmethod
    def get_latest_3_posts():
        return Post.objects.order_by('-published_at').filter(
            Q(valid_from=None) | Q(valid_from__lte=timezone.now()),
            Q(valid_to=None) | Q(valid_to__gte=timezone.now()),
        ).all()[:3]
        return Post.objects.order_by('-published_at').all()[:3]

    @staticmethod
    def get_latest_posts(n):
        return Post.objects.order_by('-published_at').filter(
            Q(valid_from=None) | Q(valid_from__lte=timezone.now()),
            Q(valid_to=None) | Q(valid_to__gte=timezone.now()),
        ).all()[:n]
        return Post.objects.order_by('-published_at').all()[:n]


    @staticmethod
    def import_bg():
        Post.objects.exclude(pk__isnull=True).delete()

        with open('mt_entry-ttl.csv', 'r', encoding='utf-8-sig') as f_src:
            src_csv = csv.DictReader(f_src, delimiter=',', quotechar='"')
            first = True
            id = 0
            for row in src_csv:
                id += 1
                post = Post()
                post.slug =  row['entry_basename']
                post.content =  row['entry_text_more']
                post.name =  row['entry_title']
                post.published_at =  datetime.datetime.strptime(row['entry_created_on'], '%Y-%m-%d %H:%M:%S')
                post.save()
            pass
        pass


    @staticmethod
    def get_sitemap_info(domain):
        return {
            'name': 'post.xml',
            'loc':  urljoin(domain, 'sitemap/post.xml'),
            'lastmod': datetime.datetime.now().isoformat()
        }

    @staticmethod
    def get_sitemap(domain, priority):
        sitemap = [{
            'loc': urljoin(domain, reverse('news.index')),
            'lastmod': datetime.datetime.now().isoformat(),
            'priority': priority
        }]

        truncate_date_y = connection.ops.date_trunc_sql('year', 'published_at')
        truncate_date_m = connection.ops.date_trunc_sql('month', 'published_at')

        qs = Post.objects.filter(published_at__gte='2011-10-29').extra({'year': truncate_date_y})
        years = qs.values('year').annotate(Count('pk')).order_by('year')

        for year in years:
            y = year['year'].year
            sitemap.append({
                'loc':urljoin(domain, reverse('news.digest_year', kwargs={'year':y})),
                'lastmod': datetime.datetime.now().isoformat(),
                'priority':priority
            })

            qs = Post.objects.filter(published_at__gte='2011-10-29').filter(published_at__year=y).extra({'month': truncate_date_m})
            monthes = qs.values('month').annotate(Count('pk')).order_by('month')

            for month in monthes:
                m = month['month'].month
                sitemap.append({
                    'loc': urljoin(domain, reverse('news.digest_month', kwargs={'year': y, 'month': m})),
                    'lastmod': datetime.datetime.now().isoformat(),
                    'priority': priority
                })

        for url in Post.objects.all():
            sitemap.append({
                'loc':urljoin(domain, url.get_canonical()),
                'lastmod': url.published_at.isoformat()+'T00:00:00.000000',
                'priority':priority*0.8
            })
        return sitemap