from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils.safestring import mark_safe
from django.template import loader
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.conf import settings
from pages.models import Page
from orders.models import Order, Cargo
from mymessages.models import Message
from testimonials.models import Testimonial
import os

# Create your views here.

def front_page(request):
    testimonials = Testimonial.objects.order_by('-id').all()[:20]
    return render(request, 'website/front-page.html', {
        'testimonials':testimonials,
    })


def uslugi_page(request):
    page = Page.objects.filter(slug='uslugi').first()
    childs = page.get_children()
    if page:
        return render(request, 'pages/content_page.html', {
            'page':page,
            'listchilds':True,
            'childs':childs
        })
    return no_page_found(request, "page with id=["+str(pk)+"] was not found")

def page_by_id(request, pk):
    page = Page.objects.filter(pk=pk).first()
    if page:
        return render(request, 'pages/content_page.html', {
            'page':page
        })
    return no_page_found(request, "page with id=["+str(pk)+"] was not found")

def page_by_slug(request, slug):
    landing = Landingpage.objects.filter(slug=slug).first()
    if landing:
        return render(request, 'website/landing_page.html', {
            'landing':landing
        })
    page = Page.objects.filter(slug=slug).first()
    if page:
        return render(request, 'pages/content_page.html', {
            'page': page
        })
    return no_page_found(request, "no landing no page with slug=[" + slug + "] was not found")

def about_page(request):
    return render(request, 'website/about.html', {
    })

def persdata_page(request):
    return render(request, 'website/persdata.html', {
    })

def sitemap(request):
    pages = Page.objects.all()
    landings = Landingpage.objects.all()
    content = loader.render_to_string('website/block_sitemap.html', {
        'pages': pages,
        'landings': landings,
    })
    return  mark_safe(content)

def no_page_found(request, errormsg):
    return  render(request, 'website/no_page_found.html', {
        'errormsg':errormsg
    })

def get_contact():
    return Contact.get_active()


def contacts(request):

    if request.method == 'GET':
        form = ContactForm()
        return render(request, "website/contacts.html", {
            'form':form,
        })

    form = ContactForm(request.POST)

    if form.is_valid():
        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        message = 'От: '+name+'\n' + 'Телефон: '+phone+'\n' + 'E-mail: ' + email + '\n' + message

        try:
            send_mail('Письмо с сайта', message, settings.DEFAULT_FROM_EMAIL, [ settings.FEEDBACK_EMAIL ])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        return redirect(reverse('website.feedback_ok'))

    return redirect(reverse('website.feedback_ok'))


def feedback_ok(request):
    return  render(request, 'website/feedback_ok.html', {
    })

def feedback_fail(request):
    return  render(request, 'website/feedback_fail.html', {
    })

def test_page(request):
    pass

def profile(request):
    return render(request, 'website/cabinet/profile.html', {

    })

@login_required
def cabinet_page(request):

    orders = Order.objects.filter(user=request.user).order_by('-id').all()[:3]
    cargos = Cargo.objects.filter(order__user=request.user).order_by('-id').all()[:3]
    messages = Message.objects.filter(user=request.user).order_by('-id').all()[:3]

    return render(request, 'website/cabinet/index.html', {
        'user': request.user,
        'orders': orders,
        'cargos': cargos,
        'messages': messages,
    })


def jstester(request):
    return render(request, 'website/jstest.html')

