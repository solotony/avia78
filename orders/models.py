from django.db import models

from datetime import datetime
from myuser.models import User
from random import randint
from django.shortcuts import reverse

def base36encode(number):
    """Converts an integer into a base36 string."""

    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if not isinstance(number, int):
        raise TypeError('This function must be called on an integer.')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(ALPHABET):
        return sign + ALPHABET[number]

    while number != 0:
        number, i = divmod(number, len(ALPHABET))
        base36 = ALPHABET[i] + base36

    return sign + base36

class Tk(models.Model):

    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Наименование',
        help_text='не более 100 символов',
    )

    class Meta:
        verbose_name = 'Перевозчик'
        verbose_name_plural = 'Перевозчики'
        ordering = ('title',)

    def __str__(self):
        return self.title

class Country(models.Model):

    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Наименование',
        help_text='не более 100 символов',
    )

    b_from = models.BooleanField(
        verbose_name='Откуда',
        help_text='Точка отправления груза',
    )

    b_to = models.BooleanField(
        verbose_name='Куда',
        help_text='Точка назначения груза',
    )

    d_from = models.BooleanField(
        verbose_name='Откуда по умолчанию',
        help_text='По умолчанию точка отправления',
        default=False,
    )

    d_to = models.BooleanField(
        verbose_name='Куда по умолчанию',
        help_text='По умолчанию точка назначения',
        default=False,
    )

    sort_order = models.IntegerField(
        verbose_name='Порядок сортировки',
        help_text='Укажите порядок сотировки если хотите принудительно управлять порядком. По умолчанию сортирует в алфавитном поряд',
        default=0,
    )

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('sort_order', 'title',)

    def __str__(self):
        return self.title


class Price(models.Model):
    c_from = models.ForeignKey(
        Country,
        null=False,
        blank=False,
        verbose_name='Откуда',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='f_prices',
    )
    c_to = models.ForeignKey(
        Country,
        null=False,
        blank=False,
        verbose_name='Куда',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='c_prices',
    )
    price_a_kg0 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена авиа (минимальная)',
        max_digits=8,
        decimal_places=2
    )
    price_a_kg1 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена/кг авиа от 100 кг',
        max_digits=8,
        decimal_places=2
    )
    price_a_kg3 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена/кг авиа от 300 кг',
        max_digits=8,
        decimal_places=2
    )
    price_a_kg5 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена/кг авиа от 500 кг',
        max_digits=8,
        decimal_places=2
    )
    price_a_kg = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена/кг  авиа от 1000 кг',
        max_digits=8,
        decimal_places=2
    )

    price_a_m3 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Ценам куб авиа',
        max_digits = 8,
        decimal_places = 2
    )

    price_s_m3 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена/м куб. море',
        max_digits = 8,
        decimal_places = 2
    )

    price_s_kg0 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена море (минимальная)',
        max_digits=8,
        decimal_places=2
    )
    price_s_kg1 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена/кг море от 100 кг',
        max_digits=8,
        decimal_places=2
    )
    price_s_kg3 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена/кг море от 300 кг',
        max_digits=8,
        decimal_places=2
    )
    price_s_kg5 = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена/кг море от 500 кг',
        max_digits=8,
        decimal_places=2
    )

    price_s_kg = models.DecimalField(
        null=True,
        blank=True,
        verbose_name='Цена/кг море от 1000 кг',
        max_digits = 8,
        decimal_places = 2
    )
    days_a = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Срок перевозки авиа',
    )
    days_s = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Срок перевозки морем',
    )


class Type(models.Model):

    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Наименование',
        help_text='не более 100 символов',
    )

    percent = models.IntegerField(
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Таможенный тариф',
        help_text='целое количество %',
    )

    class Meta:
        verbose_name = 'Вид груза'
        verbose_name_plural = 'Виды груза'
        ordering = ('title', )

    def __str__(self):
        return self.title


class Order(models.Model):

    BY_AIR = 'AIR'
    BY_SEA = 'SEA'
    BY_AUTO = 'AUTO'
    BY_TRIAN = 'TRIAN'
    BY_HORSE = 'HORSE'
    BY_OTHER = 'OTHER'

    BY_CHOICES = (
        (BY_AIR, 'Авиа перевозка'),
        (BY_SEA, 'Морская перевозка'),
        (BY_AUTO, 'Авто перевозка'),
        (BY_TRIAN, 'Ж/Д перевозка'),
        (BY_HORSE, 'Мультимодальная перевозка'),
        (BY_OTHER, 'Прочая перевозка'),
    )

    ALL_COUNTRIES = (
        ('Абхазия', 'Абхазия'),
        ('Австралия', 'Австралия'),
        ('Австрия', 'Австрия'),
        ('Азербайджан', 'Азербайджан'),
        ('Албания', 'Албания'),
        ('Алжир', 'Алжир'),
        ('Ангилья', 'Ангилья'),
        ('Ангола', 'Ангола'),
        ('Андорра', 'Андорра'),
        ('Антарктика', 'Антарктика'),
        ('Антигуа и Барбуда', 'Антигуа и Барбуда'),
        ('Аргентина', 'Аргентина'),
        ('Армения', 'Армения'),
        ('Аруба', 'Аруба'),
        ('Афганистан', 'Афганистан'),
        ('Багамские Острова', 'Багамские Острова'),
        ('Бангладеш', 'Бангладеш'),
        ('Барбадос', 'Барбадос'),
        ('Бахрейн', 'Бахрейн'),
        ('Беларусь', 'Беларусь'),
        ('Белиз', 'Белиз'),
        ('Бельгия', 'Бельгия'),
        ('Бенин', 'Бенин'),
        ('Бермудские Острова', 'Бермудские Острова'),
        ('Болгария', 'Болгария'),
        ('Боливия', 'Боливия'),
        ('Босния и Герцеговина', 'Босния и Герцеговина'),
        ('Ботсвана', 'Ботсвана'),
        ('Бразилия', 'Бразилия'),
        ('Британская территория в Индийском океане', 'Британская территория в Индийском океане'),
        ('Британские Виргинские острова', 'Британские Виргинские острова'),
        ('Бруней', 'Бруней'),
        ('Буркина-Фасо', 'Буркина-Фасо'),
        ('Бурунди', 'Бурунди'),
        ('Бутан', 'Бутан'),
        ('Вануату', 'Вануату'),
        ('Великобритания', 'Великобритания'),
        ('Венгрия', 'Венгрия'),
        ('Венесуэла', 'Венесуэла'),
        ('Виргинские острова', 'Виргинские острова'),
        ('Внешние малые острова США', 'Внешние малые острова США'),
        ('Восточное Самоа', 'Восточное Самоа'),
        ('Восточный Тимор', 'Восточный Тимор'),
        ('Вьетнам', 'Вьетнам'),
        ('Габон', 'Габон'),
        ('Гаити', 'Гаити'),
        ('Гайана', 'Гайана'),
        ('Гамбия', 'Гамбия'),
        ('Гана', 'Гана'),
        ('Гваделупа', 'Гваделупа'),
        ('Гватемала', 'Гватемала'),
        ('Гвинея', 'Гвинея'),
        ('Гвинея-Бисау', 'Гвинея-Бисау'),
        ('Германия', 'Германия'),
        ('Гернси', 'Гернси'),
        ('Гибралтар', 'Гибралтар'),
        ('Гондурас', 'Гондурас'),
        ('Гонконг', 'Гонконг'),
        ('Гренада', 'Гренада'),
        ('Гренландия', 'Гренландия'),
        ('Греция', 'Греция'),
        ('Грузия', 'Грузия'),
        ('Гуам', 'Гуам'),
        ('Дания', 'Дания'),
        ('Джерси', 'Джерси'),
        ('Джибути', 'Джибути'),
        ('Доминика', 'Доминика'),
        ('Доминиканская Республика', 'Доминиканская Республика'),
        ('Донецкая Народная Республика', 'Донецкая Народная Республика'),
        ('Египет', 'Египет'),
        ('Замбия', 'Замбия'),
        ('Западная Сахара', 'Западная Сахара'),
        ('Западный берег реки Иордан', 'Западный берег реки Иордан'),
        ('Зимбабве', 'Зимбабве'),
        ('Израиль', 'Израиль'),
        ('Индия', 'Индия'),
        ('Индонезия', 'Индонезия'),
        ('Иордания', 'Иордания'),
        ('Ирак', 'Ирак'),
        ('Иран', 'Иран'),
        ('Ирландия', 'Ирландия'),
        ('Исландия', 'Исландия'),
        ('Испания', 'Испания'),
        ('Италия', 'Италия'),
        ('Йемен', 'Йемен'),
        ('Кабо-Верде', 'Кабо-Верде'),
        ('Казахстан', 'Казахстан'),
        ('Каймановы острова', 'Каймановы острова'),
        ('Камбоджа', 'Камбоджа'),
        ('Камерун', 'Камерун'),
        ('Канада', 'Канада'),
        ('Катар', 'Катар'),
        ('Кения', 'Кения'),
        ('Кипр', 'Кипр'),
        ('Кирибати', 'Кирибати'),
        ('Китай', 'Китай'),
        ('Кокосовые острова', 'Кокосовые острова'),
        ('Колумбия', 'Колумбия'),
        ('Коморские Острова', 'Коморские Острова'),
        ('Конго, Демократическая Республика', 'Конго, Демократическая Республика'),
        ('Конго, Республика', 'Конго, Республика'),
        ('Корейская Народно-Демократическая Республика', 'Корейская Народно-Демократическая Республика'),
        ('Косово', 'Косово'),
        ('Коста-Рика', 'Коста-Рика'),
        ('Кот-д’Ивуар', 'Кот-д’Ивуар'),
        ('Куба', 'Куба'),
        ('Кувейт', 'Кувейт'),
        ('Кыргызстан', 'Кыргызстан'),
        ('Кюрасао', 'Кюрасао'),
        ('Лаос', 'Лаос'),
        ('Латвия', 'Латвия'),
        ('Лесото', 'Лесото'),
        ('Либерия', 'Либерия'),
        ('Ливан', 'Ливан'),
        ('Ливия', 'Ливия'),
        ('Литва', 'Литва'),
        ('Лихтенштейн', 'Лихтенштейн'),
        ('Луганская Народная Республика', 'Луганская Народная Республика'),
        ('Люксембург', 'Люксембург'),
        ('Маврикий', 'Маврикий'),
        ('Мавритания', 'Мавритания'),
        ('Мадагаскар', 'Мадагаскар'),
        ('Майотта', 'Майотта'),
        ('Макао', 'Макао'),
        ('Македония', 'Македония'),
        ('Малави', 'Малави'),
        ('Малайзия', 'Малайзия'),
        ('Мали', 'Мали'),
        ('Мальдивы', 'Мальдивы'),
        ('Мальта', 'Мальта'),
        ('Марокко', 'Марокко'),
        ('Мартиника', 'Мартиника'),
        ('Маршалловы острова', 'Маршалловы острова'),
        ('Мексика', 'Мексика'),
        ('Метрополия Франции', 'Метрополия Франции'),
        ('Мозамбик', 'Мозамбик'),
        ('Молдова', 'Молдова'),
        ('Монако', 'Монако'),
        ('Монголия', 'Монголия'),
        ('Монтсеррат', 'Монтсеррат'),
        ('Мьянма', 'Мьянма'),
        ('Намибия', 'Намибия'),
        ('Науру', 'Науру'),
        ('Непал', 'Непал'),
        ('Нигер', 'Нигер'),
        ('Нигерия', 'Нигерия'),
        ('Нидерланды', 'Нидерланды'),
        ('Никарагуа', 'Никарагуа'),
        ('Ниуэ', 'Ниуэ'),
        ('Новая Зеландия', 'Новая Зеландия'),
        ('Новая Каледония', 'Новая Каледония'),
        ('Норвегия', 'Норвегия'),
        ('Объединенные Арабские Эмираты', 'Объединенные Арабские Эмираты'),
        ('Оман', 'Оман'),
        ('Остров Буве', 'Остров Буве'),
        ('Остров Мэн', 'Остров Мэн'),
        ('Остров Норфолк', 'Остров Норфолк'),
        ('Остров Рождества', 'Остров Рождества'),
        ('Остров Херд и острова Макдональд', 'Остров Херд и острова Макдональд'),
        ('Острова Кука', 'Острова Кука'),
        ('Острова Питкэрн', 'Острова Питкэрн'),
        ('Острова Святой Елены, Вознесения и Тристан-да-Кунья', 'Острова Святой Елены, Вознесения и Тристан-да-Кунья'),
        ('Пакистан', 'Пакистан'),
        ('Палау', 'Палау'),
        ('Панама', 'Панама'),
        ('Папуа – Новая Гвинея', 'Папуа – Новая Гвинея'),
        ('Парагвай', 'Парагвай'),
        ('Перу', 'Перу'),
        ('Польша', 'Польша'),
        ('Португалия', 'Португалия'),
        ('Пуэрто-Рико', 'Пуэрто-Рико'),
        ('Республика Корея', 'Республика Корея'),
        ('Реюньон', 'Реюньон'),
        ('Россия', 'Россия'),
        ('Руанда', 'Руанда'),
        ('Румыния', 'Румыния'),
        ('Сальвадор', 'Сальвадор'),
        ('Самоа', 'Самоа'),
        ('Сан-Марино', 'Сан-Марино'),
        ('Сан-Томе и Принсипи', 'Сан-Томе и Принсипи'),
        ('Саудовская Аравия', 'Саудовская Аравия'),
        ('Свазиленд', 'Свазиленд'),
        ('Святой Престол (город-государство Ватикан)', 'Святой Престол (город-государство Ватикан)'),
        ('Северные Марианские острова', 'Северные Марианские острова'),
        ('Сейшельские острова', 'Сейшельские острова'),
        ('Сектор Газа', 'Сектор Газа'),
        ('Сен-Бартелеми', 'Сен-Бартелеми'),
        ('Сен-Мартен', 'Сен-Мартен'),
        ('Сен-Пьер и Микелон', 'Сен-Пьер и Микелон'),
        ('Сенегал', 'Сенегал'),
        ('Сент-Винсент и Гренадины', 'Сент-Винсент и Гренадины'),
        ('Сент-Китс и Невис', 'Сент-Китс и Невис'),
        ('Сент-Люсия', 'Сент-Люсия'),
        ('Сербия', 'Сербия'),
        ('Сингапур', 'Сингапур'),
        ('Синт-Мартен', 'Синт-Мартен'),
        ('Сирия', 'Сирия'),
        ('Словакия', 'Словакия'),
        ('Словения', 'Словения'),
        ('Соединенные Штаты Америки', 'Соединенные Штаты Америки'),
        ('Соломоновы Острова', 'Соломоновы Острова'),
        ('Сомали', 'Сомали'),
        ('Судан', 'Судан'),
        ('Суринам', 'Суринам'),
        ('Сьерра-Леоне', 'Сьерра-Леоне'),
        ('Таджикистан', 'Таджикистан'),
        ('Таиланд', 'Таиланд'),
        ('Тайвань', 'Тайвань'),
        ('Танзания', 'Танзания'),
        ('Теркс и Кайкос', 'Теркс и Кайкос'),
        ('Того', 'Того'),
        ('Токелау', 'Токелау'),
        ('Тонга', 'Тонга'),
        ('Тринидад и Тобаго', 'Тринидад и Тобаго'),
        ('Тувалу', 'Тувалу'),
        ('Тунис', 'Тунис'),
        ('Туркменистан', 'Туркменистан'),
        ('Турция', 'Турция'),
        ('Уганда', 'Уганда'),
        ('Узбекистан', 'Узбекистан'),
        ('Украина', 'Украина'),
        ('Уоллис и Футуна', 'Уоллис и Футуна'),
        ('Уругвай', 'Уругвай'),
        ('Фарерские острова', 'Фарерские острова'),
        ('Федеративные Штаты Микронезии', 'Федеративные Штаты Микронезии'),
        ('Фиджи', 'Фиджи'),
        ('Филиппины', 'Филиппины'),
        ('Финляндия', 'Финляндия'),
        ('Фолклендские острова (Мальвинские острова)', 'Фолклендские острова (Мальвинские острова)'),
        ('Франция', 'Франция'),
        ('Французская Гвиана', 'Французская Гвиана'),
        ('Французская Полинезия', 'Французская Полинезия'),
        ('Французские Южные и Антарктические территории', 'Французские Южные и Антарктические территории'),
        ('Хорватия', 'Хорватия'),
        ('Центральноафриканская Республика', 'Центральноафриканская Республика'),
        ('Чад', 'Чад'),
        ('Черногория', 'Черногория'),
        ('Чешская Республика', 'Чешская Республика'),
        ('Чили', 'Чили'),
        ('Швейцария', 'Швейцария'),
        ('Швеция', 'Швеция'),
        ('Шпицберген', 'Шпицберген'),
        ('Шри-Ланка', 'Шри-Ланка'),
        ('Эквадор', 'Эквадор'),
        ('Экваториальная Гвинея', 'Экваториальная Гвинея'),
        ('Эритрея', 'Эритрея'),
        ('Эстония', 'Эстония'),
        ('Эфиопия', 'Эфиопия'),
        ('Южная Георгия и Южные Сандвичевы острова', 'Южная Георгия и Южные Сандвичевы острова'),
        ('Южно-Африканская Республика', 'Южно-Африканская Республика'),
        ('Южная Осетия', 'Южная Осетия'),
        ('Южный Судан', 'Южный Судан'),
        ('Ямайка', 'Ямайка'),
        ('Япония', 'Япония')
    )

    created_at = models.DateTimeField(
        verbose_name='Время создания',
        default=datetime.now
    )

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        verbose_name='Заказчик',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='orders',
    )

    type = models.ForeignKey(
        Type,
        null=True,
        blank=False,
        verbose_name='Вид груза',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='orders',
    )

    trby = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        default=BY_AIR,
        verbose_name='Тип перевозки',
        choices=BY_CHOICES
    )

    type_name = models.CharField(
        max_length=60,
        null=True,
        blank=True,
        verbose_name='Наименование груза',
    )

    countryFrom = models.ForeignKey(
        Country,
        null=False,
        blank=False,
        verbose_name='Страна отправки',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='orders_f',
    )

    countryTo = models.ForeignKey(
        Country,
        null=False,
        blank=False,
        verbose_name='Страна доставки',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='orders_t',
    )

    otherCountryFrom = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Другие страны (откуда)',
        choices=ALL_COUNTRIES
    )
    otherCountryFrom
    otherCountryTo = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Другие страны (куда)',
        choices=ALL_COUNTRIES
    )

    addressFrom=models.CharField(
        null=True,
        blank=True,
        max_length=300,
        verbose_name='Адрес забора груза',
        help_text='указывается по необходимости, не более 300 символов'
    )

    addressTo=models.CharField(
        null=True,
        blank=True,
        max_length=300,
        verbose_name='Адрес доставки груза',
        help_text='указывается по необходимости, не более 300 символов'
    )

    description = models.TextField(
        verbose_name='Описание груза, дополнительные требования и пожелания',
        blank=True,
        null=True,
        max_length=20000,
        help_text='не более 20000 символов',
    )

    weight = models.IntegerField(
        verbose_name='Вес',
        blank=True,
        null=True,
        help_text='вес груза в килограммах',
    )

    volume = models.DecimalField(
        verbose_name='Объем',
        blank=True,
        null=True,
        help_text='объем груза в метрах кубических',
        decimal_places=2,
        max_digits=10,
    )

    value = models.IntegerField(
        verbose_name='Стоимость груза',
        blank=True,
        null=True,
        help_text='стоимость груза в долларах',
    )

    customs_needed = models.BooleanField(
        verbose_name='Требуется растаможка',
        help_text='требуются услуги по растамаживанию груза',
    )

    price = models.IntegerField(
        verbose_name='Стоимость перевозки',
        blank=True,
        null=True,
        help_text='стоимость перевозки в долларах',
    )

    price_include_customs = models.BooleanField(
        verbose_name='Растаможка',
        blank=False,
        null=False,
        default=False,
        help_text='стоимость включает услуги по растамаживанию груза',
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-pk',)

    def __str__(self):
        return 'Заказ № ' + str(self.pk) + ' от ' + self.created_at.date().strftime("%d.%m.%Y")

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        #TODO notify here
        pass

    def getUrl(self):
        return reverse('orders.cabinet_show', args=[self.id])

    def country_from(self):
        if self.otherCountryFrom:
            return self.otherCountryFrom
        return self.countryFrom.title

    def country_to(self):
        if self.otherCountryTo:
            return self.otherCountryTo
        return self.countryTo.title

class Cargo(models.Model):

    def getCode(self):
        return 'STA-'+base36encode((self.pk *2147483647)%9369319)+'-'+base36encode(randint(1000000, 9000000))

    created_at = models.DateTimeField(
        verbose_name='Время создания',
        default=datetime.now
    )

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='cargos',
    )

    code = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Код груза (внутренний)',
        help_text='формируется автоматически',
    )

    code_tk = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Код груза у перевозчика',
        help_text='',
    )

    tk = models.ForeignKey(
        Tk,
        null=True,
        blank=True,
        verbose_name='Перевозчик',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='cargos',
    )

    title = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Наименование груза',
        help_text='не более 500 символов',
    )

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'
        ordering = ('-pk',)

    def __str__(self):
        return 'Груз № ' + str(self.pk) + ' от ' + self.created_at.date().strftime("%d.%m.%Y")

    def save(self, *args, **kwargs):
        super(Cargo, self).save(*args, **kwargs)
        if not self.code:
            self.code = self.getCode()
            super(Cargo, self).save(*args, **kwargs)
        # TODO notify here

    def getUrl(self):
        return reverse('orders.cabinet_cargo_show', args=[self.id])

class CargoStatus(models.Model):
    STATUS_NONE = 'NONE'
    STATUS_PREPARE = 'PREPARE'
    STATUS_GOT = 'GOT'
    STATUS_TRANSPORT = 'TRANSPORT'
    STATUS_ARRIVED = 'ARRIVED'
    STATUS_CUSTOMS = 'CUSTOMS'
    STATUS_CUSTOMS_OK = 'CUSTOMS_OK'
    STATUS_READY = 'READY'
    STATUS_FINISHED = 'FINISHED'
    STATUS_SORT = 'SORT'
    STATUS_TRANSIT = 'TRANSIT'

    STATUS_CHOICES = (
        (STATUS_NONE, '--- выберите статус ---'),
        (STATUS_PREPARE, 'Забирается перевозчиком'),
        (STATUS_GOT, 'Получен перевозчиком'),
        (STATUS_TRANSPORT, 'Находится в пути в стран назначения'),
        (STATUS_ARRIVED, 'Прибыл в страну назначения'),
        (STATUS_CUSTOMS, 'Ожидает таможенной очистки'),
        (STATUS_CUSTOMS_OK, 'Выпущено таможней'),
        (STATUS_SORT, 'Поступило на сортировочный узел'),
        (STATUS_TRANSIT, 'Прибыло в транзитный город'),
        (STATUS_READY, 'Готов к получению'),
        (STATUS_FINISHED, 'Получен'),
    )

    STATUS_CHOICES_N = {
        STATUS_PREPARE: 'Забирается перевозчиком',
        STATUS_GOT:  'Получен перевозчиком',
        STATUS_TRANSPORT:  'Находится в пути в страну назначения',
        STATUS_ARRIVED:  'Прибыл в страну назначения',
        STATUS_CUSTOMS: 'Ожидает таможенной очистки',
        STATUS_CUSTOMS_OK: 'Выпущено таможней',
        STATUS_SORT: 'Поступило на сортировочный узел',
        STATUS_TRANSIT: 'Прибыло в транзитный город',
        STATUS_READY : 'Готов к получению',
        STATUS_FINISHED: 'Получен',
    }

    cargo = models.ForeignKey(
        Cargo,
        null=False,
        blank=False,
        verbose_name='Груз',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='cargo_statuses',
    )

    created_at = models.DateTimeField(
        verbose_name='Время создания статуса',
        default=datetime.now
    )

    status = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        default=STATUS_NONE,
        choices=STATUS_CHOICES
    )

    class Meta:
        verbose_name = 'Статус груза'
        verbose_name_plural = 'Статус груза'
        ordering = ('-pk',)

    def __str__(self):
        return self.created_at.__format__("%d.%m.%Y") + ' ' +  self.STATUS_CHOICES_N[self.status]