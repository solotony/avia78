from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if user.org_inn or user.org_name:
            user.is_org = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True) # changes email to unique and blank to false

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    address = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='адрес',
        help_text='адрес для доставки, не более 200 символов',
    )

    phone = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        verbose_name='телефон',
        help_text='ваш контактный номер, не более 20 символов',
    )

    is_org = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        verbose_name='организация',
        help_text='организация или частное лицо',
    )

    org_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='наименование организациии (ИП)',
        help_text='заполните если вы представитель организации, если вы частное лицо - оставьте поле пустым. не более 255 символов ',
        error_messages =    {
            'null': 'This field cannot be null.ss1',
            'blank': 'This field cannot be blank.ss2',
            'required': 'this field is requiredss3',
        }
    )

    org_inn = models.CharField(
        max_length=12,
        blank=True,
        unique=True,
        null=True,
        verbose_name='ИНН организациии',
        help_text='заполните если вы представитель организации, если вы частное лицо - оставьте поле пустым. 10-12 цифр ',
        validators=[
            RegexValidator(
                regex='^[0-9]{10}(:?[0-9]{2})?$',
                message='Инн должен состоять из 10 ити 12 цифр',
                code='invalid_inn'
            ),
        ]
    )

    PT_ROZNITSA = 'R'
    PT_MOPT = 'M'
    PT_OPT = 'O'
    PRICE_TYPE_CHOICES = (
        (PT_ROZNITSA, 'Розница'),
        (PT_MOPT, 'Мелкий Опт'),
        (PT_OPT, 'Опт')
    )

    price_type = models.CharField(
        max_length=1,
        choices=PRICE_TYPE_CHOICES,
        default=PT_ROZNITSA,
        verbose_name='тип цен',
    )

    price_discount = IntegerRangeField(
        verbose_name='скидка, %',
        default=0,
        min_value=0,
        max_value=50
    )

    objects = UserManager()  # This is the new line in the User model. #

    def __str__(self):
        return self.get_print_name()

    def get_print_name(self):

        if self.org_name and (self.org_name!='') :
            return self.org_name

        if self.first_name or self.last_name:
            return self.first_name + ' ' + self.last_name

        return self.email


    @staticmethod
    def register(name, email, phone, plain_password):
        if User.objects.filter(email=email).first():
            return None
        user = User()
        user.last_name = name
        user.email = email
        user.phone = phone
        user.set_password(plain_password)
        user.save()
        #TODO notification
        return user