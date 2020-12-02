from django.shortcuts import render
from .models import Page

def no_page_found(request, errormsg):
    return  render(request, 'website/no_page_found.html', {
        'errormsg':errormsg
    })

def page_by_id(request, pk):
    page = Page.objects.filter(pk=pk).first()
    if page:
        return render(request, 'website/content_page.html', {
            'page':page
        })
    return no_page_found(request, "page with id=["+str(pk)+"] was not found")


def page_by_slug(request, slug):
    page = Page.objects.filter(fullslug=slug).first()
    if page:
        return render(request, 'website/content_page.html', {
            'page': page,
        })
    return no_page_found(request, "no landing no page with slug=[" + slug + "] was not found")


