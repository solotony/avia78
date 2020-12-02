from django.db import models
from django.utils.html import mark_safe
from django.urls import reverse
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.fields import ThumbnailerImageField
from mptt.models import MPTTModel, TreeForeignKey
#from pricelist.models import PriceEntry
from random import randint
from time import strftime
from ckeditor_uploader.fields import RichTextUploadingField
import datetime
#from django.contrib.contenttypes.fields import GenericRelation
from common.models import get_upload_path
from gallery.models import GalleryCategory
from urllib.parse import urljoin
import os
import re

class Page(MPTTModel):

    TAIL_SLASH = '/'
    TAIL_PHP = '.php'
    TAIL_HTML = '.html'
    TAIL_INDEX_HTML = '/index.html'
    TAIL_INDEX_PHP = '/index.php'

    TAILS =(
        (TAIL_SLASH, TAIL_SLASH),
        (TAIL_PHP, TAIL_PHP),
        (TAIL_HTML, TAIL_HTML),
        (TAIL_INDEX_HTML, TAIL_INDEX_HTML),
        (TAIL_INDEX_PHP, TAIL_INDEX_PHP),
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name='Родитель',
        on_delete=models.SET_NULL,
        db_index=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = [ 'name', ]

    slug = models.SlugField(
        max_length=84,
        null=False,
        blank=False,
        verbose_name='относительный ЧПУ',
    )

    fullslug = models.SlugField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        verbose_name='полный ЧПУ',
    )

    canonical_tail = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        default=TAIL_SLASH,
        choices=TAILS,
        verbose_name='окончание канонического ЧПУ',
    )

    name = models.CharField(
        max_length=300,
        verbose_name='название страницы',
        help_text='не более 100 символов, используется для манипуляции со страницей, '
                  'а также по умолчанию в качестве title, description, header'
    )

    title = models.CharField(
        null=True,
        blank=True,
        max_length=300,
        verbose_name='поле title страницы',
        help_text='не более 300 символов, по умолчанию будет использовано "название страницы" '
                  '(если не знаете что это такое - спросите у своего SEO-шника)'
    )

    description = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='поле description страницы',
        help_text='не более 500 символов, по умолчанию будет использовано "название страницы" '
                  '(если не знаете что это такое - спросите у своего SEO-шника)'
    )

    anchor_short = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        verbose_name='коороткая ссылка',
        help_text='текст ссылки длиной до 30 символов, данная текст используется там где место ограничено (в меню и т.д.)'
    )

    anchor_full = models.CharField(
        null=True,
        blank=True,
        max_length=150,
        verbose_name='длинная ссылка',
        help_text='текст ссылки длиной до 150 символов'
    )

    header = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='основной заголовок страницы',
        help_text='не более 200 символов, по умолчанию будет использовано "название страницы"'
    )

    subheader = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='подзаголовок страницы',
        help_text='не более 200 символов'
    )

    promotext = models.TextField(
        null=True,
        blank=True,
        max_length=1000,
        verbose_name='промо текст в верхнюю часть страницы',
        help_text='не более 1000 символов'
    )

    safetext = models.TextField(
        null=True,
        blank=True,
        max_length=50000,
        verbose_name='html текст в верхнюю часть страницы (под промотекст). Сюда вставляются коды JS для карт или прочего',
        help_text='не более 50000 символов'
    )

    content = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name='Содержимое страницы')

    show_childs = models.BooleanField(
        default = False,
        verbose_name='Отображать список дочерних страниц',
        help_text = 'после основного содержимого можно вывести список страниц раздела. Страницы выводятся "плашками".'
    )

    hide_in_parent_list = models.BooleanField(
        default=False,
        verbose_name='Не показывать в списке родительской страницы',
        help_text = 'Этот пункт надо отметить, что бы не выводить ссылку на эту стараницу в списке дочерних страниц '
                    'у родительской страницы.'
    )

    show_frontimage = models.BooleanField(
        default=False,
        verbose_name='Отображать крупное изображение в начале страницы'
    )

    embed_documents = models.BooleanField(
        default=False,
        verbose_name='Встраивать прикрепленные документы в текст страницы'
    )

    favorite_page = models.BooleanField(
        default=False,
        verbose_name='Избранная',
        help_text = 'Избранная страница, для отображения на главной'
    )

    def _get_upload_path(instance, filename):
        return get_upload_path('pages', filename)

    image = ThumbnailerImageField(
        null=True,
        blank=True,
        verbose_name='Основное изображение страницы',
        help_text='размеры изображения на странице -  1170x550 (обрезается), '
                  'в списке страниц или новостей - 348x220 (обрезается)',
        upload_to=_get_upload_path,
    )

    attached_gallery = models.ForeignKey(
        GalleryCategory,
        null=True,
        blank=True,
        verbose_name='галерея',
        on_delete=models.SET_NULL
    )

    def image_tag(self):
        if (self.image):
            thumb_url = get_thumbnailer(self.image.name)['admin'].url
            return mark_safe('<img src="%s" />' % thumb_url)
        return None

    image_tag.short_description = 'Превью'
    image_tag.allow_tags = True

    def image_thumb_url(self):
        if (self.image):
            return get_thumbnailer(self.image.name)['page.thumb'].url
        return None

    def image_full_url(self):
        if (self.image):
            return get_thumbnailer(self.image.name)['page.full'].url
        return None

    def __str__(self):
        return self.name + ' (' + self.fullslug  + ')'

    def get_title(self):
        if (self.title):
            return self.title
        return self.name

    def get_descriptopn(self):
        if (self.description):
            return self.description
        return self.name

    def get_header(self):
        if (self.header):
            return self.header
        return self.name

    def get_anchor_short(self):
        if (self.anchor_short):
            return self.anchor_short
        return self.name[:30]

    def get_anchor_full(self):
        if (self.anchor_full):
            return self.anchor_full
        return self.name

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ('name',)

    def get_url(self):
        if self.fullslug:
            if self.canonical_tail == self.TAIL_PHP:
                return reverse('pages.page_by_slug_php', args=(self.fullslug,))
            elif self.canonical_tail == self.TAIL_HTML:
                return reverse('pages.page_by_slug_html', args=(self.fullslug,))
            else:
                return reverse('pages.page_by_slug', args=(self.fullslug,))
        return reverse('pages.page_by_id', args=(self.id,))

    def related_label(self):
        return u"%s (%s)" % (self.name, self.id)

    def children_to_show(self):
        return self.children.filter(hide_in_parent_list=False)

    def get_admin_edit(self):
        r = str(randint(10000000,99999999))
        return mark_safe('<a href="/admin/pages/page/'+str(self.id)+'/change/" style="background-color: #000;color:#CC0000; padding:6px;">редактировать</a> ' \
               '<script id="rand'+r+'">document.getElementById("rand'+r+'").parentNode.style.border = "4px dashed #CC0000";</script>')

    def get_docs_all(self):
        return Document.objects.filter(page=self).order_by('-uploaded').all()

    def reset_years(self):
        Document.staticYears = {}
        return ''

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.parent:
                self.fullslug = self.parent.fullslug + '/' + self.slug
            else:
                self.fullslug = self.slug
            pass
        super(Page, self).save(*args, **kwargs)

    pages = []

    @staticmethod
    def create_page(file, title, description, content):
        content = re.sub('@@@@', "\n", content)
        content = re.sub('@@', "\n", content)
        content = re.sub('&nbsp;', " ", content, flags=re.MULTILINE)
        content = re.sub('<p.*?/>\s*<p.*?/>', "<br />", content, flags=re.MULTILINE)
        content = re.sub('<br.*?/>\s*<br.*?/>', "<br />", content, flags=re.MULTILINE)
        content = re.sub('<div.*?>', " ", content)
        content = re.sub('</div.*?>', " ", content)

        if  file.startswith('/news/') or  file.startswith('/2010/') or  file.startswith('/2011/') or \
            file.startswith('/2012/') or  file.startswith('/2013/') or  file.startswith('/2014/') or \
            file.startswith('/2015/') : return

        if file.startswith('/'):
            file = file[1:]

        canonic_tail = '/'
        if file.endswith('/index.php'):
            canonic_tail = '/'
            file = file[:-10]
        elif file.endswith('/index.html'):
            canonic_tail = '/index.html'
            file = file[:-11]
        elif file.endswith('.html'):
            canonic_tail = '.html'
            file = file[:-5]
        elif file.endswith('.php'):
            canonic_tail = '.php'
            file = file[:-4]
        elif file.endswith('/'):
            canonic_tail = '/'
            file = file[:-1 ]
        else:
            canonic_tail = '/'

        with open('tmp.txt', 'a+', encoding='windows-1251') as f:
            print (canonic_tail, file, file=f)

        file_a = file.split('/')

        parent = None
        for slug in file_a[:-1]:
            if not parent:
                x = Page.objects.filter(fullslug=slug).first()
            else:
                x = parent.children.filter(slug=slug).first()

            if not x:
                print('CREATE PARENT' + file + ' ' + slug)
                x = Page()
                x.title = slug
                x.description = slug
                x.content = slug
                x.slug = slug
                x.name = slug
                if parent:
                    x.parent = parent
                    x.fullslug = parent.fullslug + x.slug
                else:
                    x.fullslug = x.slug
                x.save()
            parent = x

        slug = file_a[-1]

        if not parent:
            x = Page.objects.filter(fullslug=slug).first()
        else:
            x = parent.children.filter(slug=slug).first()

        if not x:
            print('CREATE ' + file)
            x = Page()
            x.title = 'autogen ' + slug
            x.slug = slug
            x.title = title
            x.description = description
            x.content = content
            x.name = title
            if parent:
                x.parent = parent
                x.fullslug = parent.fullslug + x.slug
            else:
                x.fullslug = x.slug
            x.save()
        else:
            print ('DUPA ' + file)


    @staticmethod
    def import_bg():
        Page.objects.exclude(pk__isnull=True).delete()
        with open('res.txt', 'r', encoding='windows-1251') as f:
            file = None
            title = None
            description = None
            content = None
            for str in f:
                str.encode('utf8')
                str = str.rstrip()
                if str.startswith('file:'):
                    file = str[6:]
                    continue
                if str.startswith('title:'):
                    title = str[7:]
                    continue
                if str.startswith('description:'):
                    description = str[13:]
                    continue
                if str.startswith('content:'):
                    content = str[9:]
                    if file and title:
                        Page.create_page(file, title, description, content)

                    file = None
                    title = None
                    description = None
                    content = None
                    continue
                pass
        pass

        Page.objects.rebuild()

    @staticmethod
    def get_sitemap_info(domain):
        return {
            'name': 'page.xml',
            'loc': urljoin(domain, 'sitemap/page.xml'),
            'lastmod': datetime.datetime.now().isoformat()
        }

    @staticmethod
    def get_sitemap(domain, priority):
        sitemap = []
        for url in Page.objects.all():
            sitemap.append({
                'loc': urljoin(domain, url.get_url()),
                'lastmod': datetime.datetime.now().isoformat(),
                'priority': priority
            })
        return sitemap

class Document(models.Model):

    page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        verbose_name='Страница',
        on_delete=models.SET_NULL,
        db_index=True,
        related_name='docs',
    )

    name = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='название документа',
        help_text='не более 500 символов'
    )

    def _get_upload_path(instance, filename):
        return get_upload_path('documents', filename)

    file = models.FileField(
        null=False,
        blank=False,
        verbose_name='файл документа',
        upload_to=_get_upload_path,
    )

    uploaded = models.DateField(
        null=False,
        blank=False,
        verbose_name='загружен',
        default=datetime.date.today,
    )

    def __str__(self):
        if self.name:
            return self.name
        return self.file.name

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ('name',)

    def get_url(self, mode=None):
        return self.file.url

    ext_to_icon = {
        'pdf':'pdf.svg',
        'doc':'docx.svg',
        'docx':'docx.svg',
        'rtf':'rtf.svg',
        'default':'default.svg'
    }

    def get_icon(self):
        iconname = self.ext_to_icon['default']
        file_name, file_ext = os.path.splitext(self.file.name)
        file_ext = file_ext[1:].lower()
        if file_ext in self.ext_to_icon:
            iconname = self.ext_to_icon[file_ext]
       #return mark_safe('<img src="/static/website/i/icons/'+iconname+'" alt="" /> ('+ self.file.name + ' | ' +  file_name+ ' | ' +file_ext +')')
        return mark_safe('<img src="/static/website/i/icons/' + iconname + '"alt="" />')

    staticYears = {}

    @staticmethod
    def _is_new_year(year):
        if year in Document.staticYears.keys():
            return False
        return True

    def is_new_year(self):
        return Document._is_new_year(self.uploaded.year)

    def get_year(self):
        year = self.uploaded.year
        Document.staticYears[year] = year
        return year
