from django.shortcuts import render
from website.views import sitemap as website_sitemap
from django.utils.safestring import mark_safe

# Create your views here.

def sitemap_page(request):
    return render(request, 'common/sitemap.html', {
        'sitemaps':(
            sitemap(request),
            website_sitemap(request),
        ),
    })

def sitemap(request):
    return mark_safe('')
