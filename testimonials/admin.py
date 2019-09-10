from django.contrib import admin
from .models import Testimonial

class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
    list_display = ('name', 'created_at', 'moderated')
    list_editable = ('moderated',)
    fields = (
        'name',
        'text',
        'moderated',
        'created_at',
        #('image', 'image_tag'),
        ('scan', 'scan_tag')
    )
    readonly_fields = ('image_tag', 'scan_tag')

admin.site.register(Testimonial, TestimonialAdmin)
