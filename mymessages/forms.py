from django.forms import ModelForm, BooleanField, CharField
from .models import Message

class MessageFromSite(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'text']

    register = BooleanField(
        label='Зарегистрироваться на сайте',
        help_text='Зарегистрируйтесь на сайте что бы получить весь комплекс услуг',
        required = False
    )

    def __init__(self, *args, **kwargs):
        super(MessageFromSite, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['text'].required = True

class MessageFromCabinet(ModelForm):
    class Meta:
        model = Message
        fields = ['text']


class DocQueryFromSite(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone']

    order_id = CharField(
        label='Номер заказа',
        help_text='Укажите номер заказа, для которого вам необходимы бухгалтерские документы',
        required=True
    )

    register = BooleanField(
        label='Зарегистрироваться на сайте',
        help_text='Зарегистрируйтесь на сайте что бы получить весь комплекс услуг',
        required = False
    )

    def __init__(self, *args, **kwargs):
        super(DocQueryFromSite, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True

class DocQueryFromCabinet(ModelForm):
    class Meta:
        model = Message
        fields = []

    order_id = CharField(
        label='Номер заказа',
        help_text='Укажите номер заказа, для которого вам необходимы бухгалтерские документы',
        required=True
    )