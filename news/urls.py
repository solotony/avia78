from django.urls import path, re_path
from . import views

urlpatterns = [

    path('<int:year>/<int:month>/<slug>.html', views.post_detail_ym, name='news.post_detail_html'),
    path('<int:year>/<int:month>/<slug>/', views.post_detail_ym, name='news.post_detail_new'),
    path('<int:year>/<int:month>/', views.digest_month, name='news.digest_month'),
    path('<int:year>/', views.digest_year, name='news.digest_year'),
    path('', views.index, name='news.index'),
    path('search/', views.search, name='news.search'),
    path('<slug>/', views.post_detail, name='news.post_detail_canonical'),

]