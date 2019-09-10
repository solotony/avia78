from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.categories, name='gallery.categories'),
    url(r'^category/(?P<pk>\d+)/$', views.category, name='gallery.category'),
    url(r'^(?P<slug>\S+)/$', views.category_by_slug, name='gallery.category_by_slug'),
]