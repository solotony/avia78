from django.urls import path, re_path, reverse
from . import views

urlpatterns = [
    path('cargo/<int:cargo_id>/', views.cargo_show, name='orders.cabinet_cargo_show'),
    path('<int:order_id>/', views.order_show, name='orders.cabinet_show'),
    path('create/', views.order_create, name='orders.cabinet_create'),
    path('cargo/', views.cargo_index, name='orders.cabinet_cargo_index'),
    path('', views.order_index, name='orders.cabinet_index'),
]