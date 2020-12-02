from django.forms import ModelForm, CharField, EmailField
from .models import Order, Country
from django.forms.utils import ErrorDict, ErrorList, pretty_name  # NOQA

class CabinetOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['countryFrom', 'otherCountryFrom', 'addressFrom',
                  'countryTo', 'otherCountryTo', 'addressTo',
                  'trby', 'type_name', 'description', 'weight', 'volume', 'value',
                  'customs_needed']

    def __init__(self, *args, **kwargs):
        super(CabinetOrderForm, self).__init__(*args, **kwargs)
        self.fields['countryFrom'].queryset = Country.objects.filter(b_from=True)
        self.fields['countryTo'].queryset = Country.objects.filter(b_to=True)

    def _full_clean(self):
        super(CabinetOrderForm, self).full_clean()
        self._errors = ErrorDict()

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['countryFrom', 'otherCountryFrom', 'addressFrom',
                  'countryTo', 'otherCountryTo', 'addressTo',
                  'trby', 'type_name', 'description', 'weight', 'volume', 'value',
                  'customs_needed']

    name = CharField(
        label='Ваше имя',
        help_text='Укажите ваше имя оформлени заказа',
        required=True
    )

    email = EmailField(
        label='E-mail',
        help_text='Укажите вашу электронную почту для отправки документов',
        required=True
    )

    phone = CharField(
        label='Телефон',
        help_text='Укажите ваш телефон для связи',
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['countryFrom'].queryset = Country.objects.filter(b_from=True)
        self.fields['countryTo'].queryset = Country.objects.filter(b_to=True)

    def _full_clean(self):
        super(OrderForm, self).full_clean()
        self._errors = ErrorDict()

class OrderFormLt(ModelForm):
    class Meta:
        model = Order
        fields = ['countryFrom', 'otherCountryFrom',
                  'countryTo', 'otherCountryTo',
                  'trby', 'weight', 'volume', 'type_name',
                  'customs_needed']

    name = CharField(
        label='Ваше имя',
        help_text='Укажите ваше имя',
        required=True
    )

    email = EmailField(
        label='E-mail',
        help_text='Укажите вашу электронную почту для получения расчета',
        required=True
    )

    phone = CharField(
        label='Телефон',
        help_text='Укажите ваш телефон для связи',
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(OrderFormLt, self).__init__(*args, **kwargs)
        self.fields['countryFrom'].queryset = Country.objects.filter(b_from=True)
        self.fields['countryTo'].queryset = Country.objects.filter(b_to=True)

    def _full_clean(self):
        super(OrderFormLt, self).full_clean()
        self._errors = ErrorDict()


class CalcForm(ModelForm):
    class Meta:
        model = Order
        fields = ['description', 'countryFrom', 'countryTo', 'trby', 'type_name', 'weight', 'volume', 'value', 'customs_needed']

    name = CharField(
        label='Ваше имя',
        help_text='Укажите ваше имя для оформления заказа',
        required=False
    )

    email = EmailField(
        label='E-mail',
        help_text='Укажите вашу электронную почту для отправки документов',
        required=False
    )

    phone = CharField(
        label='Телефон',
        help_text='Укажите ваш телефон для связи',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(CalcForm, self).__init__(*args, **kwargs)
        self.fields['countryFrom'].queryset = Country.objects.filter(b_from=True)
        self.fields['countryTo'].queryset = Country.objects.filter(b_to=True)