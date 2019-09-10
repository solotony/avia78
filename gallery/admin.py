from django.contrib import admin
from .models import *

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3
    fields = ('name', 'image', 'image_tag', 'sort_order')
    readonly_fields = ('image_tag', )

class GalleryCategoryAdmin(admin.ModelAdmin):
    model = GalleryCategory
    prepopulated_fields = {'slug': ('name',), }
    fields = ('name', 'slug', 'title', 'description', 'header', 'abstract', 'orient')
    inlines = [PhotoInline, ]
    list_display= ['name', 'slug', ]
    search_fields = ['name']
    #admin_order_field = ('name')

admin.site.register(GalleryCategory, GalleryCategoryAdmin)