from django.contrib import admin
from .models import *
from django_mptt_admin.admin import DjangoMpttAdmin

class ContactAdmin(admin.ModelAdmin):
    model = Contact
    extra = 1

    fieldsets = (
        (None, {
            'fields': ('company_name', 'frontpage', 'phone1', 'phone2', 'email', 'address', 'map',
                       'active', 'slogan', ('logo', 'logo_tag'), 'main_menu', 'menu_services', 'menu_countries', 'menu_articles'
                )
        }),
        # ('текст на страницу "контакты"', {
        #     'classes': ('collapse',),
        #     'fields': ('htext_contacts',)
        # }),
        # ('текст на страницу "о нас"', {
        #     'classes': ('collapse',),
        #     'fields': ('htext_about',)
        # }),
        # ('текст на страницу "политика обработки персональных данных"', {
        #     'classes': ('collapse',),
        #     'fields': ('htext_persdata',)
        # }),
        ('Социальные сети', {
            'classes': ('collapse',),
            'fields': ('facebook', 'vk', 'instagram', 'twitter', 'googleplus', 'youtube', 'odnoklassniki')
        }),
    )

    readonly_fields = ('logo_tag',)
    list_display = ['company_name', 'phone1', 'email', 'active']

class AdvantageInline(admin.TabularInline):
    model = Advantage
    extra = 1
    fields = ( 'title', 'iconimg', 'iconimg_tag', 'text', 'url')
    readonly_fields = ('iconimg_tag',)

class TextonmainInline(admin.TabularInline):
    model = Textonmain
    extra = 1
    fields = ('name','text')

class LandingpageAdmin(admin.ModelAdmin):
    model = Landingpage
    actions_on_bottom = True
    actions_on_top = False
    list_display= ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',), }
    inlines = [TextonmainInline,AdvantageInline,]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),

#        ('Основной контент', {
#            'fields': ('helo_text', 'subhelo_text', 'content_text',),
#        }),

        ('SEO', {
#            'classes': ('collapse',),
            'fields': ('title', 'description'),
        }),

#        ('Верхний слайдер', {
#            'classes': ('collapse', 'extrapretty'),
#            'fields': ('slides', ),
#        }),

    )
    readonly_fields = ('content_image_tag',)

class SlideAdmin(admin.ModelAdmin):
    model = Slide
    list_display = ['name', 'background_tag']
    fieldsets = (
        (None, {
            'fields': (
                'name',
#                'type',
                ('background', 'background_tag')
            )
        }),
#        ('Баннер', {
#            'fields': ('header', 'text1', 'text2', 'text3', 'action_url', 'action_text'),
#        }),
    )
    readonly_fields = ('background_tag',)



#admin.site.register(Slide, SlideAdmin)
admin.site.register(Landingpage, LandingpageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Textonmain)