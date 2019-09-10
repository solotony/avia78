from django.urls import path, re_path, reverse
from . import views

urlpatterns = [
    path('from/',       views.countries_from,   name='api.countries_from'),
    path('to/',         views.countries_to,     name='api.countries_to'),
    path('prices/',     views.prices,           name='api.prices'),
    path('search/',     views.search,           name='api.search'),
]