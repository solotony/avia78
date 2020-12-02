from django.urls import path, re_path, reverse
from . import views

urlpatterns = [
    path('create/', views.order_create, name='orders.create'),
    path('created/', views.created, name='orders.created'),
    path('calculator/', views.order_create_lt, name='orders.calculator'),
    path('calculator-ex/', views.calculator_page, name='orders.calculator_ex'),
    path('cargo/<cargo_code>/', views.cargo_info, name='orders.cargoinfo'),
]