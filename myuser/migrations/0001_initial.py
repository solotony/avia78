# Generated by Django 2.0.2 on 2019-03-25 15:13

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import myuser.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('address', models.CharField(blank=True, help_text='адрес для доставки, не более 200 символов', max_length=200, null=True, verbose_name='адрес')),
                ('phone', models.CharField(help_text='ваш контактный номер, не более 20 символов', max_length=20, verbose_name='телефон')),
                ('is_org', models.BooleanField(default=False, help_text='организация или частное лицо', verbose_name='организация')),
                ('org_name', models.CharField(blank=True, error_messages={'blank': 'This field cannot be blank.ss2', 'null': 'This field cannot be null.ss1', 'required': 'this field is requiredss3'}, help_text='заполните если вы представитель организации, если вы частное лицо - оставьте поле пустым. не более 255 символов ', max_length=255, null=True, verbose_name='наименование организациии (ИП)')),
                ('org_inn', models.CharField(blank=True, help_text='заполните если вы представитель организации, если вы частное лицо - оставьте поле пустым. 10-12 цифр ', max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_inn', message='Инн должен состоять из 10 ити 12 цифр', regex='^[0-9]{10}(:?[0-9]{2})?$')], verbose_name='ИНН организациии')),
                ('price_type', models.CharField(choices=[('R', 'Розница'), ('M', 'Мелкий Опт'), ('O', 'Опт')], default='R', max_length=1, verbose_name='тип цен')),
                ('price_discount', myuser.models.IntegerRangeField(default=0, verbose_name='скидка, %')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', myuser.models.UserManager()),
            ],
        ),
    ]
