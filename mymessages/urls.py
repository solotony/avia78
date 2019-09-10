from django.urls import path, re_path, reverse
from . import views

urlpatterns = [
    path('query/', views.create, name='messages.query'),
    path('doc-query/', views.create_doc, name='messages.doc_query'),
    path('call-query/', views.create_query, name='messages.call_query'),
    path('created/', views.created, name='messages.created'),
]