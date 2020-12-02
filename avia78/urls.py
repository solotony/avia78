"""avia78 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from filebrowser.sites import site as filebrowsersite
from django.contrib.auth import views as authviews
from django.conf.urls.static import static
from django.conf import settings
from website import views as website_views

urlpatterns = [
    path('jstester/', website_views.jstester, name='website.jstester'),

    re_path('ckeditor/', include('ckeditor_uploader.urls')),
    path('genrelview/', include("genericrelationview.urls")),
    path('admin/filebrowser/', filebrowsersite.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),
    re_path('^accounts/login/$', authviews.LoginView.as_view(), name='login'),
    re_path('^accounts/logout/$', authviews.LogoutView.as_view(), name='logout'),

    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('user/', include('myuser.urls')),
    path('message/', include('mymessages.urls')),
    path('testimonial/', include('testimonials.urls')),
    path('order/', include('orders.urls')),
    path('cabinet/message/', include('mymessages.cabinet_urls')),
    path('cabinet/order/', include('orders.cabinet_urls')),
    path('cabinet/profile/', include('myuser.cabinet_urls')),
    path('cabinet/', include('website.cabinet_urls')),
    path('sitemap.xml', include('sitemap.urls')),
    path('sitemap/', include('sitemap.urls')),
    path('', include('website.urls')),
    path('', include('pages.urls')),


    #path('cabinet/order/', include('website.urls')),
    #path('cabinet/cargo/', include('website.urls')),
    # path('cabinet/cargo/',  order.cargo-urls),

]

urlpatterns += static(settings.STATIC_URL , document_root = settings.STATIC_ROOT )
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
