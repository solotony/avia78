from django.contrib import admin
from .models import Country, Cargo, CargoStatus, Order, Type, Tk, Price
from django.forms import TextInput, Textarea, NumberInput
from django.db import models

# Register your models here.

class TkAdmin(admin.ModelAdmin):
    model = Tk
    list_display= ['title',]

class PricesFromInline(admin.TabularInline):
    model = Price
    fk_name = 'c_from'
    extra = 1
    fields = ('c_to',
              'price_a_kg1', 'price_a_kg3', 'price_a_kg5', 'price_a_kg', 'price_a_kg0', 'days_a',
              'price_s_kg1', 'price_s_kg3', 'price_s_kg5', 'price_s_kg', 'price_s_kg0', 'days_s' )
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(PricesFromInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'c_to':
            field.queryset = field.queryset.filter(b_to=True)
        return field
    verbose_name = "Цены на перевозку из "
    verbose_name_plural = "Цены на перевозку из "

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '6'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.IntegerField: {'widget': NumberInput(attrs={'size': '10', 'style': 'width:10ch'})},
        models.DecimalField: {'widget': NumberInput(attrs={'size': '10', 'style': 'width:10ch'})},
    }

class PricesToInline(admin.TabularInline):
    model = Price
    fk_name = 'c_to'
    extra = 1
    fields = ('c_from',
              'price_a_kg1', 'price_a_kg3', 'price_a_kg5', 'price_a_kg', 'price_a_kg0', 'days_a',
              'price_s_kg1', 'price_s_kg3', 'price_s_kg5', 'price_s_kg', 'price_s_kg0', 'days_s' )
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(PricesToInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'c_from':
            field.queryset = field.queryset.filter(b_from=True)
        return field
    verbose_name = "Цены на перевозку в "
    verbose_name_plural =  "Цены на перевозку в "

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '6'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.IntegerField: {'widget': NumberInput(attrs={'size': '10', 'style': 'width:10ch'})},
        models.DecimalField: {'widget': NumberInput(attrs={'size': '10', 'style': 'width:10ch'})},
    }

class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display= ['title', 'b_from', 'b_to', 'sort_order']
    fields = ['title', 'b_from', 'b_to', 'sort_order']
    inlines = [PricesFromInline, PricesToInline]

class TypeAdmin(admin.ModelAdmin):
    model = Type
    list_display = ['title', 'percent', ]

class CargoInline(admin.TabularInline):
    model = Cargo
    extra = 1
    fields = ('title', 'code', 'tk', 'code_tk')
    readonly_fields = ('code', )

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['__str__', 'user','countryFrom', 'countryTo', ]
    readonly_fields = ('created_at', 'user',)
    fieldsets = (
        (None, {
            'fields': (('created_at', 'user',), )
        }),
        ('Параметры заказа', {
           'fields': (('countryFrom', 'otherCountryFrom',), 'addressFrom',
                      ('countryTo', 'otherCountryTo', ), 'addressTo',
                      'type', 'description', ('weight', 'volume', 'value', 'customs_needed',))
        }),
        ('Заполняется менеджером', {
            'fields': (('price', 'price_include_customs',), ),
        }),
    )
    inlines = [CargoInline, ]

class AddCargoStatusInline(admin.TabularInline):
    model = CargoStatus
    extra = 0
    fields = ('created_at', 'status', )
    readonly_fields =  ('created_at', )
    def has_change_permission(self, request, obj=None):
        return False
    def has_view_permission(request, obj=None, dummy=None):
        return False
    verbose_name = "Установить новый статус"
    verbose_name_plural = "Установить новый статус"

class CargoStatusInline(admin.TabularInline):
    model = CargoStatus
    extra = 0
    fields = ('created_at', 'status', )
    readonly_fields =  ('created_at', 'status', )
    def has_add_permission(self, request):
        return False
    def has_view_permission(request, obj=None, dummy=None):
        return False

class CargoAdmin(admin.ModelAdmin):
    model = Cargo
    list_display = ['id', 'order', 'title', 'code', 'tk', 'code_tk',]
    fields = ('order', 'title', 'code', 'tk', 'code_tk' )
    readonly_fields = ('code', 'order')
    inlines = [CargoStatusInline, AddCargoStatusInline, ]

class PriceAdmin(admin.ModelAdmin):
    model = Price

admin.site.register(Order, OrderAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Tk, TkAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Price, PriceAdmin)

