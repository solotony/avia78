# Generated by Django 2.0.2 on 2019-03-25 15:14

import datetime
from django.db import migrations, models
import easy_thumbnails.fields
import news.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='уникальный адрес страницы')),
                ('name', models.CharField(help_text='не более 100 символов, используется для манипуляции с новостью, а также по умолчанию в качестве title, description, header', max_length=100, verbose_name='название новости')),
                ('title', models.CharField(blank=True, help_text='не более 300 символов, по умолчанию будет использовано "название новости" (если не знаете что это такое - спросите у своего SEO-шника)', max_length=300, null=True, verbose_name='поле title новости')),
                ('description', models.CharField(blank=True, help_text='не более 500 символов, по умолчанию будет использован "анонс новости", а при его отсутствии - "название новости"  (если не знаете что это такое - спросите у своего SEO-шника)', max_length=500, null=True, verbose_name='поле description новости')),
                ('header', models.CharField(blank=True, help_text='не более 200 символов, по умолчанию будет использовано "название новости"', max_length=200, null=True, verbose_name='основной заголовок новости')),
                ('abstract', models.TextField(blank=True, help_text='не более 500 символов, по умолчанию будут использованы первые ч00 знаков "текста новости". анонс не выводится на странице с текстом новости', max_length=500, null=True, verbose_name='анонс новости')),
                ('content', models.TextField(blank=True, help_text='если это поле пустое, то прикрепленное изображение выводится по центру на всю страницу', null=True, verbose_name='текст новости')),
                ('published_at', models.DateField(default=datetime.date.today, verbose_name='дата публикации')),
                ('valid_from', models.DateField(blank=True, help_text='дата, начиная с которой включительно новость отображается', null=True, verbose_name='с')),
                ('valid_to', models.DateField(blank=True, help_text='дата, до которой включительно новость отображается', null=True, verbose_name='до')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, help_text='размеры изображения на странице новости -  770x562 (обрезается), в списке новостей - 370x270 (обрезается)', null=True, upload_to=news.models.Post.get_upload_path, verbose_name='Основное изображение новости')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ('-published_at',),
            },
        ),
    ]
