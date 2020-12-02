# Generated by Django 2.1.7 on 2019-06-09 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_auto_20190609_1820'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('sort_order', 'title'), 'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AddField(
            model_name='country',
            name='sort_order',
            field=models.IntegerField(default=0, help_text='Укажите порядок сотировки если хотите принудительно управлять порядком. По умолчанию сортирует в алфавитном поряд', verbose_name='Порядок сортировки'),
        ),
    ]
