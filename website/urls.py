from django.urls import path, re_path, reverse
from . import views

urlpatterns = [
    path('', views.front_page, name='website.front'),
]