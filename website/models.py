from django.db import models
from tinymce import HTMLField
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.fields import ThumbnailerImageField
import os
from time import strftime
from random import randint
from django.utils.html import mark_safe
from django.urls import reverse
from menu.models import MenuItem
import re
from mptt.models import MPTTModel, TreeForeignKey
from gallery.models import Photo, GalleryCategory
from news.models import Post
from pages.models import Page
from testimonials.models import Testimonial
from urllib.parse import urljoin
from datetime import datetime

#
# cтраницы адресуются по id как /pages/{id}
# или от корня как /{slug}
#

class Slide(models.Model):
    SLIDE_SIMPLE = 'SS'
    SLIDE_WITH_BANNER = 'SB'
    SLIDE_TYPES_CHOICES = (
        (SLIDE_SIMPLE, 'Простой слайд'),
        (SLIDE_WITH_BANNER, 'Слайд с баннером'),
    )
    type = models.CharField(
        max_length=2,
        choices=SLIDE_TYPES_CHOICES,
        default=SLIDE_SIMPLE,
    )

    def get_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return os.path.join(
            "media/slides/", strftime("%Y/%m/%d/"), str(randint(10000000, 99999999)) + file_extension)

    background = ThumbnailerImageField(
        null=True,
        blank=True,
        verbose_name='Фон слайда',
        upload_to=get_upload_path,
        help_text=''
    )

    def background_tag(self):
        if (self.background):
            thumb_url = get_thumbnailer(self.background.name)['admin'].url
            return  mark_safe('<img src="%s" />' % thumb_url)
        return None

    background_tag.short_description = 'Загруженное изображение'
    background_tag.allow_tags = True

    def get_background_url(self):
        if (self.background):
            return get_thumbnailer(self.background.name)['slide_background'].url
        return None

    name = models.CharField(
        max_length=100,
        verbose_name='название слайда',
    )

    header = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='заголовок баннера',
    )

    text1 = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='текст 1-я строка баннера',
    )

    text2 = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='текст 2-я строка баннера',
    )

    text3 = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='текст 3-я строка баннера',
    )

    action_url = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='URL действия',
        help_text='URL кнопки, телефона (в зависимости от макета)'
    )

    action_text = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='текст действия',
        help_text='текст кнопки, телефона (в зависимости от макета)'
    )

    def __str__(self):
        return self.name

    def with_banner(self):
        return self.type == self.SLIDE_WITH_BANNER

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'


class Landingpage(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name='название страницы',
    )

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
        verbose_name='поле title страницы',
        help_text='не более 300 символов, по умолчанию будет использовано '
                  '"название страницы" (если не знаете что это такое - спросите у своего SEO-шника)'
    )

    description = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='поле description страницы',
        help_text='не более 500 символов, по умолчанию будет использовано '
                  '"название страницы" (если не знаете что это такое - спросите у своего SEO-шника)'
    )

    helo_text = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name='приветствие',
        help_text='не более 50 символов'
    )

    subhelo_text = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='под приветствие',
        help_text='не более 100 символов'
    )

    content_text = models.TextField(
        null=True,
        blank=True,
        max_length=5000,
        verbose_name='Основной текст',
        help_text='не более 5000 символов. на странице текст выводится в 2 колонки, разбиваясь на 2 более-менее '
                  'равные части. Для принудительного разбиения поставьте символ "#" (решетка)'
    )

    def content_text_first(self):
        m = self.content_text.find('#')
        if m != -1:
            return self.content_text[:m]
        l = len(self.content_text)
        m = int(l/2)
        while self.content_text[m] != ' ':
            m += 1
        return self.content_text[:m]

    def content_text_second(self):
        m = self.content_text.find('#')
        if m != -1:
            return self.content_text[m+1:]

        l = len(self.content_text)
        m = int(l/2)
        while self.content_text[m] != ' ':
            m += 1
        return self.content_text[m+1:]

    ##########################################################

    slides = models.ManyToManyField(
        Slide,
        blank=True,
        verbose_name='слайды',
        related_name='pages')

    ##########################################################

    use_testimonial_section = models.BooleanField(
        default=True,
        verbose_name='Секция "Полезные советы"',
    )

    testimonial_header = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Заголовок секции')


    ##########################################################

    use_fp_section = models.BooleanField(
        default=True,
        verbose_name='Секция "Избранные страницы"',
    )


    fp_header = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Заголовок секции')

    fp_action_url = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='ссылка URL')

    fp_action_text = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Текст кнопки')


    def get_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return os.path.join(
            "media/lcontent/", strftime("%Y/%m/%d/"), str(randint(10000000, 99999999)) + file_extension)

    content_image = ThumbnailerImageField(
        null=True,
        blank=True,
        verbose_name='Основное изображение',
        upload_to=get_upload_path,
        help_text=''
    )

    def content_image_tag(self):
        thumb_url = get_thumbnailer(self.content_image.name)['admin'].url
        return mark_safe('<img src="%s" />' % thumb_url)

    content_image_tag.short_description = 'Превью'
    content_image_tag.allow_tags = True

    def content_image_url(self):
        return get_thumbnailer(self.content_image.name)['content_image'].url



    ##########################################################

    use_cta_section = models.BooleanField(
        default=True,
        verbose_name='Секция "Призыв к действию"',
    )

    cta_header = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Заголовок секции')

    cta_text = models.TextField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='Текст секции призыв к действию')

    cta_action_url = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='ссылка URL')

    cta_action_text = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Текст кнопки')


    ##########################################################

    use_persons_section = models.BooleanField(
        default=True,
        verbose_name='Секция "Персонал"',
    )

    persons_header = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Заголовок секции')

    ##########################################################

    use_banners_section = models.BooleanField(
        default=True,
        verbose_name='Секция "Баннеры"',
    )

    banners_header = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Заголовок секции')

    ##########################################################

    use_userhtml_section = models.BooleanField(
        default=True,
        verbose_name='Секция "Пользовательский HTML"',
    )

    userhtml_header = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Заголовок секции')

    userhtml_text = models.TextField(
        null=True,
        blank=True,
        max_length=10000,
        verbose_name='Пользовательский HTML')

    ##########################################################

    use_video_section = models.BooleanField(
        default=True,
        verbose_name='Секция "Видео"',
    )

    video_header = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Заголовок секции')

    video_1 = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Видео 1')

    video_2 = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Видео 2')

    ##########################################################

    use_news_section = models.BooleanField(
        default=True,
        verbose_name='Секция "Новости"',
    )

    news_header = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Заголовок секции')

    news_action_url = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name='ссылка URL')

    news_action_text = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Текст кнопки')

##########################################################

    def __str__(self):
        return self.name

    def get_title(self):
        if (self.title):
            return self.title
        return self.name

    def get_description(self):
        if (self.description):
            return self.description
        return self.name

    def get_header(self):
        if (self.header):
            return self.header
        return self.name

    def get_url(self):
        if (self.slug):
            return reverse('website.page_by_slug', args=(self.slug,))
        return None

    class Meta:
        verbose_name = 'Посадочная страница'
        verbose_name_plural = 'Посадочные страницы'
        ordering = ('name',)

    def get_testimonials_all(self):
        return Testimonial.objects.filter(frontpage=self).all()

    @staticmethod
    def get_sitemap_info(domain):
        return {
            'name': 'landingpage.xml',
            'loc': urljoin(domain, 'sitemap/landingpage.xml'),
            'lastmod': datetime.now().isoformat()
        }

    @staticmethod
    def get_sitemap(domain, priority):
        sitemap = [{
            'loc': urljoin(domain, ''),
            'lastmod': datetime.now().isoformat(),
            'priority': priority
        }]
        for url in Landingpage.objects.all():
            if Contact.get_frontpage() != url:
                sitemap.append({
                    'loc': urljoin(domain, url.get_url()),
                    'lastmod': datetime.now().isoformat(),
                    'priority': priority * 0.8
                })
        return sitemap


class Advantage(models.Model):

    frontpage = models.ForeignKey(
        Landingpage,
        verbose_name='посадочная страница',
        on_delete=models.DO_NOTHING,
        related_name='advantages'
    )

    iconimg = ThumbnailerImageField(
        null=True,
        blank=True,
        verbose_name='Картинка иконки',
        help_text='не более 20 символов'
    )

    icon = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Иконка',
        help_text='не более 20 символов')

    title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Заголовок',
        help_text='не более 100 символов')

    text = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Текст',
        help_text='не более 200 символов')

    url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Ссылка',
        help_text='не более 200 символов')

    def __str__(self):
        return self.title

    def get_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return os.path.join(
            "media/icon/", strftime("%Y/%m/%d/"), str(randint(10000000, 99999999)) + file_extension)

    def iconimg_tag(self):
        thumb_url = get_thumbnailer(self.iconimg.name)['admin'].url
        return  mark_safe('<img src="%s" />' % thumb_url)

    def iconimg_url(self):
        return get_thumbnailer(self.iconimg.name)['website.iconimg'].url

    iconimg_tag.short_description = 'Превью'
    iconimg_tag.allow_tags = True

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуга'

class Contact(models.Model):

    frontpage = models.ForeignKey(
        Landingpage,
        verbose_name='Лендинг',
        on_delete = models.DO_NOTHING,
        related_name='contacts'
    )

    company_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        default='наименование организации',
        verbose_name='наименование организации',
        help_text='наименование организации')

    phone1 = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        verbose_name='номер телефона СПб',
        help_text='не более 20 символов')

    phone2 = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='номер телефона Москва',
        help_text='не более 20 символов')

    email = models.EmailField(
        max_length=60,
        null=False,
        blank=False,
        verbose_name='адрес электронной почты',
        help_text='не более 60 символов')

    openings = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name='рабочее время',
        help_text='не более 40 символов')

    openings_full = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='рабочее время, полностью',
        help_text='не более 200 символов, можно использовать HTML тэги')

    facebook = models.URLField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='facebook',
        help_text='не более 120 символов')

    vk = models.URLField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='вКонтакте',
        help_text='не более 120 символов')

    instagram = models.URLField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='instagram',
        help_text='не более 120 символов')

    twitter = models.URLField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='twitter',
        help_text='не более 120 символов')

    googleplus = models.URLField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='google+',
        help_text='не более 120 символов')

    youtube = models.URLField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='youtube',
        help_text='не более 120 символов')

    odnoklassniki = models.URLField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='одноклассники ',
        help_text='не более 120 символов')

    address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='адрес',
        help_text='не более 200 символов')

    map = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='код для вставки карт на сайт',
        help_text='не более 500 символов')

    slogan = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='промо-текст в подвал',
        help_text='не более 500 символов (рекомендуется 250 и по содержанию близко к SEO-description главной страницы)')

    active = models.BooleanField(
        verbose_name='активные настройки',
        null=False,
        blank=False,
        default=False
    )

    htext_contacts = HTMLField(
        null=True,
        blank=True,
        verbose_name='HTML текст на страницу "контакты"')

    htext_about = HTMLField(
        null=True,
        blank=True,
        verbose_name='HTML текст на страницу "о нас"')

    htext_persdata = HTMLField(
        null=True,
        blank=True,
           verbose_name='HTML текст на страницу "политика обработки персональных данных"')

    def get_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return os.path.join(
            "media/logos/", strftime("%Y/%m/%d/"), str(randint(10000000, 99999999)) + file_extension)

    logo = ThumbnailerImageField(
        null=True,
        blank=True,
        verbose_name='основной логотип',
        upload_to=get_upload_path,
        help_text='соотношение сторон должно быть 315*46'
    )

    main_menu = models.ForeignKey(
        MenuItem,
        null=True,
        blank=True,
        verbose_name='Основное меню (разделы)',
        on_delete = models.SET_NULL,
        related_name='main_menu',
    )

    menu_services = models.ForeignKey(
        MenuItem,
        null=True,
        blank=True,
        verbose_name='Меню услуги',
        on_delete=models.SET_NULL,
        related_name='menu_services',
    )

    menu_countries = models.ForeignKey(
        MenuItem,
        null=True,
        blank=True,
        verbose_name='Меню страны',
        on_delete=models.SET_NULL,
        related_name='menu_countries',
    )

    menu_articles = models.ForeignKey(
        MenuItem,
        null=True,
        blank=True,
        verbose_name='Меню статьи',
        on_delete=models.SET_NULL,
        related_name='menu_articles',
    )

    gallery = models.ForeignKey(
        GalleryCategory,
        null=True,
        blank=True,
        verbose_name='Фотографии на главной',
        on_delete=models.SET_NULL
    )

    def logo_tag(self):
        thumb_url = get_thumbnailer(self.logo.name)['admin'].url
        return  mark_safe('<img src="%s" />' % thumb_url)

    logo_tag.short_description = 'Превью'
    logo_tag.allow_tags = True

    def get_logo_url(self):
        return get_thumbnailer(self.logo.name)['logo'].url

    def get_phone1_url(self):
        if self.phone1:
            return 'tel:' + re.sub(r'[^\+0-9]', '', self.phone1)
        return ''

    def get_phone2_url(self):
        if self.phone2:
            return 'tel:' + re.sub(r'[^\+0-9]', '', self.phone2)
        return ''

    def get_email_url(self):
        return 'mailto:' + self.email

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки #' + str(self.company_name)

    @staticmethod
    def get_active():
        contact = Contact.objects.order_by('-active').first()
        if (not contact):
            #raise Exception("no any contact information detected")
            return None
        return contact

    @staticmethod
    def get_frontpage():
        contact = Contact.objects.order_by('-active').first()
        if (not contact):
            #raise Exception("no any contact information detected")
            return None
        return contact.frontpage

    @staticmethod
    def get_mainmenu():
        contact =  Contact.objects.order_by('-active').first()
        if (not contact):
            #raise Exception("no any contact information detected")
            return None
        if (not contact.main_menu):
            return None
        childs = contact.main_menu.get_childs()
        return childs

    def get_photos(self):
        photos = self.gallery.get_photos_all()
        return photos

    def get_latest_8_posts(self):
        return Post.get_latest_posts(8)

    @staticmethod
    def get_favorite_pages():
        pages = Page.objects.filter(favorite_page=True).all()
        if (not pages.count):
            # raise Exception("no any contact information detected")
            return None
        return pages


def context_processors(request):
    return {
        'website_settings': Contact.get_active(),
        'website_frontpage': Contact.get_frontpage(),
        'website_mainmenu': Contact.get_mainmenu(),
    }

class SHIT001(models.Model):

    frontpage = models.ForeignKey(
        Landingpage,
        null=True,
        blank=False,
        verbose_name='посадочная страница',
        on_delete=models.DO_NOTHING,
        related_name='testimonials'
    )

    name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name='Заголовок',
        help_text='не более 30 символов')

    text = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Текст',
        help_text='не более 500 символов')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Совет'
        verbose_name_plural = 'Советы'


class Textonmain(models.Model):
    frontpage = models.ForeignKey(
        Landingpage,
        null=True,
        blank=False,
        verbose_name='посадочная страница',
        on_delete=models.DO_NOTHING,
        related_name='textonmain'
    )

    name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name='Заголовок',
        help_text='не более 30 символов')

    text = models.TextField(
        max_length=5000,
        null=True,
        blank=True,
        verbose_name='Текст',
        help_text='не более 5000 символов, допустимы символы HTML')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Текст на главной'
        verbose_name_plural = 'Тексты на главной'
