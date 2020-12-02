from django.shortcuts import render
#from gallery.models import GalleryCategory
from news.models import Post
#from pricelist.models import PriceCategory
#from staff.models import Person
from pages.models import Page
from website.models import Landingpage
from testimonials.models import Testimonial

# Create your views here.

domain = 'https://avia78.ru/'

def sitemapindex(request):
    return render(request, 'sitemap/sitemapindex.xml', {
        'sitemaps': (
            [
                #GalleryCategory.get_sitemap_info(domain),
                Post.get_sitemap_info(domain),
                #PriceCategory.get_sitemap_info(domain),
                #Person.get_sitemap_info(domain),
                Page.get_sitemap_info(domain),
                Landingpage.get_sitemap_info(domain),
                Testimonial.get_sitemap_info(domain),
            ]
        ),
        'domain': 'http://anis-clinic.ru/'
    },content_type='text/xml')

def sitemap(request,sitemapname):
    if sitemapname == Landingpage.get_sitemap_info(domain).get('name', ''):
        return render(request, 'sitemap/sitemap.xml', {
            'sitemap': Landingpage.get_sitemap(domain, 1)
        }, content_type='text/xml')

    if sitemapname == Post.get_sitemap_info(domain).get('name', ''):
        return render(request, 'sitemap/sitemap.xml', {
            'sitemap': Post.get_sitemap(domain, 0.8)
        }, content_type='text/xml')

    if sitemapname == Page.get_sitemap_info(domain).get('name', ''):
        return render(request, 'sitemap/sitemap.xml', {
            'sitemap': Page.get_sitemap(domain, 0.8)
        }, content_type='text/xml')

    if sitemapname == Testimonial.get_sitemap_info(domain).get('name', ''):
         return render(request, 'sitemap/sitemap.xml', {
             'sitemap': Testimonial.get_sitemap(domain, 0.8)
         }, content_type='text/xml')

    return render(request, 'sitemap/sitemap.xml', {
        'sitemap': [{'loc':1},{'loc':2}],
        'priority':'0.1',
    },content_type='text/xml')
