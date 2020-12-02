from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.sitemap_page, name='sitemap_page'),
]

