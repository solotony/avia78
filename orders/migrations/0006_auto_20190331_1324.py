# Generated by Django 2.0.2 on 2019-03-31 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20190331_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='code_tk',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True, verbose_name='Код груза у перевозчика'),
        ),
    ]
