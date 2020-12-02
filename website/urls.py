from django.urls import path, re_path, reverse
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.front_page, name='website.front'),
    re_path('^solotony/$', TemplateView.as_view(template_name='website/developer.html'), name='developer'),
    re_path(r'^cmsmagazinec4639f3b000df051ff472e1a11bfb147\.txt$',
            TemplateView.as_view(template_name='website/cmsmagazine.txt', content_type='text/plain')),
]
