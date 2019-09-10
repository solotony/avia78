# Generated by Django 2.0.2 on 2019-03-31 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymessages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('Вопрос с сайта', 'Вопрос с сайта'), ('Уведомление', 'Уведомление'), ('Запрос документов', 'Запрос документов'), ('Запрос расчета', 'Запрос расчета'), ('Запрос звонка', 'Запрос звонка'), ('Ответ пользователя', 'Ответ пользователя'), ('Ответ системы', 'Ответ системы')], default='Вопрос с сайта', max_length=20, verbose_name='Тип сообщения'),
        ),
    ]
