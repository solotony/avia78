from django.urls import path, re_path, reverse
from . import views

urlpatterns = [
    path('', views.cabinet_page, name='website.cabinet'),
]