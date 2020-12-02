from django.conf.urls import url
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('<int:pk>/', views.page_by_id, name='pages.page_by_id'),
    re_path(r'^(?P<slug>.*?)/$', views.page_by_slug, name='pages.page_by_slug'),
    re_path(r'^(?P<slug>.*?).html$', views.page_by_slug, name='pages.page_by_slug_html'),
    re_path(r'^(?P<slug>.*?).php$', views.page_by_slug, name='pages.page_by_slug_php'),
]
