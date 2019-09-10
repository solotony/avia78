from django.contrib import admin
from django.urls import reverse
from .models import MenuItem, FixedPage
from django_mptt_admin.admin import DjangoMpttAdmin

class MenuItemAdmin(DjangoMpttAdmin):
    model = MenuItem
    fields = ('parent', 'title', 'link', 'content_type', 'object_id' )
    related_lookup_fields = {
        'generic': [['content_type', 'object_id'], ],
    }

    def save_model(self, request, obj, form, change):
        if not obj.title:
            if obj.content_object:
                obj.title = str(obj.content_object)
            else:
                obj.title = 'пункт меню'
        super(MenuItemAdmin, self).save_model(request, obj, form, change)

    generic_pairs = (('content_type', 'object_id'),)

    def __init__(self, *args, **kwargs):
        super(MenuItemAdmin, self).__init__(*args, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        save_kwargs = dict(kwargs)
        request = kwargs.pop("request", None)
        for (content_type, object_id) in self.generic_pairs:
            if db_field.name == content_type:
                return self.formfield_for_content_type(
                    db_field, object_id, content_type, request, **kwargs
                )
            elif db_field.name == object_id:
                return self.formfield_for_object_id(db_field, request, **kwargs)
        return super(
            MenuItemAdmin, self
        ).formfield_for_dbfield(db_field, **save_kwargs)

    def formfield_for_content_type(
        self, db_field, object_id, content_type, request, **kwargs
    ):
        formfield = super(
            MenuItemAdmin, self
        ).formfield_for_foreignkey(db_field, request, **kwargs)
        widget = formfield.widget
        url = reverse('generickey_json')
        widget.attrs.update({
            'onchange': "generic_view_json(this,'{0}','{1}','{2}');".format(
                url, object_id, content_type
            ),
            'class': 'generic_view'
        })
        return formfield

    def formfield_for_object_id(self, db_field, request, **kwargs):
        return db_field.formfield(**kwargs)

    class Media:
        js = (
            'js/admin/generickey.js',
        )


# Register your models here.
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(FixedPage)

