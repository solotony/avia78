# Generated by Django 2.1.8 on 2019-05-16 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order_trby'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='d_from',
            field=models.BooleanField(default=False, help_text='По умолчанию точка отправления', verbose_name='Откуда по умолчанию'),
        ),
        migrations.AddField(
            model_name='country',
            name='d_to',
            field=models.BooleanField(default=False, help_text='По умолчанию точка назначения', verbose_name='Куда по умолчанию'),
        ),
        migrations.AlterField(
            model_name='order',
            name='trby',
            field=models.CharField(choices=[('AIR', 'Авиа перевозка'), ('SEA', 'Морская перевозка'), ('AUTO', 'Авто перевозка'), ('TRIAN', 'Ж/Д перевозка'), ('HORSE', 'Гужевая перевозка'), ('OTHER', 'Прочая перевозка')], default='AIR', max_length=6, verbose_name='Тип перевозки'),
        ),
    ]
