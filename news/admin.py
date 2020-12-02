from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    model = Post
    prepopulated_fields = {'slug': ('name',), }
    fields = ('name', 'slug', 'title', 'description', 'header', 'abstract', 'content',  'published_at',
              ('valid_from', 'valid_to'), ('image', 'image_tag') )
    readonly_fields = ('image_tag', )

    list_display= ['name', 'slug', 'published_at', 'valid_from', 'valid_to']
    search_fields = ['name']
    #admin_order_field = ('name')


admin.site.register(Post, PostAdmin)


