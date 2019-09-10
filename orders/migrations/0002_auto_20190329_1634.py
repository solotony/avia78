# Generated by Django 2.0.2 on 2019-03-29 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Types',
            new_name='Type',
        ),
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='orders.Type', verbose_name='Вид груза'),
        ),
        migrations.AlterField(
            model_name='order',
            name='countryFrom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_f', to='orders.Country', verbose_name='Страна отправки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='countryTo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_t', to='orders.Country', verbose_name='Страна доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
    ]