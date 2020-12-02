from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Page, Document

class DocumentInline(admin.TabularInline):
    model = Document
    fields = ('name', 'file', 'uploaded')
    extra = 3

class PageAdmin(DjangoMpttAdmin):
    model = Page
    #prepopulated_fields = {'slug': ('name',), }

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'parent',
                ('fullslug', 'slug', 'canonical_tail'),
                'content'
            )
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': (
                'title',
                'description',
                'header',
            ),
        }),
        ('Прочее', {
            'classes': ('collapse',),
            'fields': (
                'subheader',
                #'promotext',
                #'safetext',
                # 'price',
                # #'anchor_short',
                # #'anchor_full',
                ('image', 'image_tag'),
                'show_childs',
                'hide_in_parent_list',
                #'show_frontimage',
                'attached_gallery',
                'embed_documents',
                'favorite_page',
            ),

        }),

    )

    readonly_fields = ('image_tag', 'fullslug', )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('slug',)
        return self.readonly_fields

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        else:
            return {'slug': ('name',), }

    #fields = ('name', 'slug', 'title', 'description', 'header', 'abstract', 'content', 'published_at',
    #          ('valid_from', 'valid_to'), ('image', 'image_tag') )
    #readonly_fields = ('image_tag', )
    #
    list_display= ['name', 'slug', 'fullslug', 'image_tag']
    search_fields = ['name']
    #admin_order_field = ('name')
    inlines = [DocumentInline, ]


admin.site.register(Page, PageAdmin)
admin.site.register(Document)