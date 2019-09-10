from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<pk>/', views.testimonial, name='testimonials.show'),
    path('', views.index, name='testimonials.list'),
]
