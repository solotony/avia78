from django.contrib import admin

# Register your models here.

from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at', 'type', 'title', 'user', 'email', 'phone']



