from django.urls import path, re_path, reverse
from . import views

urlpatterns = [
    path('', views.cabinet_index, name='messages.cabinet_index'),
    path('create/', views.create, name='messages.cabinet_create'),
    path('<int:message_id>/', views.cabinet_message, name='messages.cabinet_message'),
]