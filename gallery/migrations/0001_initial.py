# Generated by Django 2.0.2 on 2019-03-25 15:14

from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import gallery.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orient', models.CharField(choices=[('S', 'Смешенная ониентация - квадратные превьюшки'), ('P', 'Портретная ониентация - вертикальные превьюшки'), ('A', 'Альбомная ориентация - горизонтальные превьюшки'), ('N', 'Смешенная ониентация - произвольные превьюшки')], default='S', max_length=1)),
                ('name', models.CharField(help_text='не более 100 символов, используется для манипуляции с категорией, а также по умолчанию в качестве title, description, header', max_length=100, verbose_name='название категории')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='уникальный адрес страницы')),
                ('title', models.CharField(blank=True, help_text='не более 300 символов, по умолчанию будет использовано "название категории" (если не знаете что это такое - спросите у своего SEO-шника)', max_length=300, null=True, verbose_name='поле title новости')),
                ('description', models.CharField(blank=True, help_text='не более 500 символов, по умолчанию будет использован "краткий текст", а при его отсутствии - "название категории"  (если не знаете что это такое - спросите у своего SEO-шника)', max_length=500, null=True, verbose_name='поле description новости')),
                ('header', models.CharField(blank=True, help_text='не более 200 символов, по умолчанию будет использовано "название категории"', max_length=200, null=True, verbose_name='основной заголовок новости')),
                ('abstract', models.TextField(blank=True, help_text='не более 500 символов ', max_length=500, null=True, verbose_name='краткий текст на страницу')),
            ],
            options={
                'verbose_name': 'Галерея',
                'verbose_name_plural': 'Галерея',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='не более 200 символов', max_length=200, verbose_name='подпись изображения')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, help_text='размеры изображения на странице новости -  770x562 (обрезается), в списке новостей - 370x270 (обрезается)', null=True, upload_to=gallery.models.Photo.get_upload_path, verbose_name='Основное изображение новости')),
                ('sort_order', models.IntegerField(default=0, verbose_name='порядок')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='gallery.GalleryCategory', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображение',
                'ordering': ('sort_order',),
            },
        ),
    ]
