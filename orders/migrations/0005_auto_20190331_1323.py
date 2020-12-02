# Generated by Django 2.0.2 on 2019-03-31 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20190331_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cargo',
            options={'ordering': ('-pk',), 'verbose_name': 'Груз', 'verbose_name_plural': 'Грузы'},
        ),
        migrations.AddField(
            model_name='cargo',
            name='code',
            field=models.CharField(db_index=True, default='111111', help_text='формируется автоматически', max_length=30, verbose_name='Код груза (внутренний)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cargo',
            name='code_tk',
            field=models.CharField(db_index=True, default='111111', max_length=30, verbose_name='Код груза у перевозчика'),
            preserve_default=False,
        ),
    ]
