# Generated by Django 2.1.8 on 2019-04-12 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20190331_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargostatus',
            name='status',
            field=models.CharField(choices=[('NONE', '--- выберите статус ---'), ('PREPARE', 'Забирается перевозчиком'), ('GOT', 'Получен перевозчиком'), ('TRANSPORT', 'Находится в пути в стран назначения'), ('ARRIVED', 'Прибыл в страну назначения'), ('CUSTOMS', 'Ожидает таможенной очистки'), ('READY', 'Готов к получению')], default='NONE', max_length=10),
        ),
    ]
