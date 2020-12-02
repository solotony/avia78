from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.sitemapindex, name='sitemapindex'),
    url(r'^(?P<sitemapname>\S+)$', views.sitemap, name='sitemap'),
]

