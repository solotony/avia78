from django.db import models

from datetime import datetime
from myuser.models import User

class Message(models.Model):

    STATUS_DRAFT = 'DRAFT'
    STATUS_SEND = 'SEND'
    STATUS_DELETED = 'DELETED'
    STATUS_READED = 'READ'
    STATUS_FLAG = 'FLAG'

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_SEND, 'Отправлено'),
        (STATUS_READED, 'Прочитано'),
        (STATUS_FLAG, 'Важное'),
        (STATUS_DELETED, 'Удалено')
    )

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name='Получатель',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='send_messages',
    )

    TYPE_QUESTION = 'Вопрос с сайта'
    TYPE_DOC_REQUEST = 'Запрос документов'
    TYPE_CALC_REQUEST = 'Запрос расчета'
    TYPE_CALL_REQUEST = 'Запрос звонка'
    TYPE_NOTIFICATION = 'Уведомление'
    TYPE_USER_MESSAGE = 'Ответ пользователя'
    TYPE_SYS_MESSAGE = 'Ответ системы'

    TYPE_CHOICES = (
        (TYPE_QUESTION, 'Вопрос с сайта'),
        (TYPE_NOTIFICATION, 'Уведомление'),
        (TYPE_DOC_REQUEST, 'Запрос документов'),
        (TYPE_CALC_REQUEST, 'Запрос расчета'),
        (TYPE_CALL_REQUEST, 'Запрос звонка'),
        (TYPE_USER_MESSAGE, 'Ответ пользователя'),
        (TYPE_SYS_MESSAGE, 'Ответ системы'),
    )

    type = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        default=TYPE_QUESTION,
        verbose_name='Тип сообщения',
        choices=TYPE_CHOICES
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='телефон',
        help_text='ваш контактный номер, не более 20 символов',
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='e-mail')

    status = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        default = STATUS_DRAFT,
        verbose_name='Статус сообщения',
        choices = STATUS_CHOICES
    )

    created_at = models.DateTimeField(
        verbose_name='Время отправки',
        default=datetime.now
    )

    name = models.CharField(
        verbose_name='Имя отправителя',
        blank=True,
        max_length=100,
        help_text='не более 100 символов',
        null=True,
    )

    title = models.CharField(
        verbose_name='Заголовок сообщения',
        blank=True,
        max_length=200,
        help_text='не более 200 символов',
        null=True,
    )

    text = models.TextField(
        verbose_name='Текст сообщения',
        blank=True,
        max_length=50000,
        help_text='не более 50000 символов',
        null=True,
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('-created_at',)

    def __str__(self):
        if (self.title):
            return self.type + ': ' + self.title
        else :
            return self.type + ' № ' + str(self.id)
