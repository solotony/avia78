# Generated by Django 2.1.8 on 2019-04-12 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20190412_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='canonical_tail',
            field=models.SlugField(choices=[('/', '/'), ('.php', '.php'), ('.html', '.html')], default='/', max_length=5, verbose_name='окончание канонического ЧПУ'),
        ),
        migrations.AlterField(
            model_name='page',
            name='fullslug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='полный ЧПУ'),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(max_length=60, unique=True, verbose_name='относительный ЧПУ'),
        ),
    ]
