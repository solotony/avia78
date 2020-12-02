from django.shortcuts import render, redirect, reverse
from .forms import OrderForm, CabinetOrderForm, CalcForm, OrderFormLt
from .models import Order, Cargo, CargoStatus, Country
from django.contrib.auth.decorators import login_required
from myuser.models import User
from django.contrib import messages
from random import randint
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.forms.utils import ErrorDict, ErrorList, pretty_name  # NOQA
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import get_template
from django.conf import settings
import random
import string

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

@login_required
def order_index(request):
    orders = Order.objects.filter(user=request.user).order_by('-id').all()
    orders = Order.objects.filter(user=request.user).order_by('-id').all()[:3]
    #paginator = Paginator(orders, 2)
    #page = request.GET.get('p')
    #orders = paginator.get_page(page)

    return render(request, 'website/cabinet/orders-index.html', {
        'orders':orders
    })

def order_create(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CabinetOrderForm(request.POST)
        else:
            form = OrderForm(request.POST, initial={})

        novalidate = int(request.POST.get('novalidate', 0))

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.user = User.objects.filter(email=form.cleaned_data.get('email')).first()

                if not order.user_id:

                    plain_password = randomStringDigits(8)

                    order.user = User.register(form.cleaned_data.get('name'), form.cleaned_data.get('email'), form.cleaned_data.get('phone'), plain_password)
                    if not order.user_id:
                        messages.add_message(request, messages.ERROR, 'Регистрация не удалась, хрень какая-то')
                        return HttpResponse('Регистрация не удалась, хрень какая-то')
                    else:
                        messages.add_message(request, messages.SUCCESS, 'Ваша заявка зарегистрирована. На вашу электронную почту выслан доступ в личный кабинет.')
                        d = {'user': order.user, 'plain_password': plain_password}
                        template_t = get_template('email/user-registered.txt')
                        message = template_t.render(d)
                        try:
                            send_mail('Регистрация на сайте', message, settings.DEFAULT_FROM_EMAIL, [order.user.email])
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                else:
                    messages.add_message(request, messages.SUCCESS,
                                         'Ваша заявка зарегистрирована')

            order.save()

            d = {'user': order.user, 'order': order}
            template_t = get_template('email/user-order-created.txt')
            template_a = get_template('email/adm-order-created.txt')
            message_a = template_a.render(d)
            message_t = template_t.render(d)
            try:
                send_mail('Заказ', message_a, settings.DEFAULT_FROM_EMAIL, [settings.NOTIFY_EMAIL])
                send_mail('Оформление заказа на сайте', message_t, settings.DEFAULT_FROM_EMAIL, [order.user.email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.add_message(request, messages.SUCCESS,
                'Ваш ' + str(order) + ' оформлен и поступил на обработку к нашим менеджерам. Обработка выполняется в '
                     'течении нескольких рабочих часов, по результатам обработки вы получите счет на '
                     'оплату услуг. В случае возникновения вопросов менеджер свяжется с вами.')

            return redirect(reverse('orders.created'))
        else:
            form._errors = ErrorDict()
            form.full_clean = form._full_clean

    else:
        if request.user.is_authenticated:
            form = CabinetOrderForm()
        else:
            form = OrderForm()

    return render(request, 'website/cabinet/orders-create.html', {
        'form':form
    })


def order_create_lt(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CabinetOrderForm(request.POST)
        else:
            form = OrderFormLt(request.POST, initial={})

        novalidate = int(request.POST.get('novalidate', 0))

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.user = User.objects.filter(email=form.cleaned_data.get('email')).first()

                if not order.user_id:
                    plain_password = randomStringDigits(8)
                    order.user = User.register(form.cleaned_data.get('name'), form.cleaned_data.get('email'), form.cleaned_data.get('phone'), plain_password)
                    if not order.user_id:
                        messages.add_message(request, messages.ERROR, 'Регистрация не удалась, хрень какая-то')
                        return HttpResponse('Регистрация не удалась, хрень какая-то')
                    else:
                        messages.add_message(request, messages.SUCCESS, 'Ваша заявка зарегистрирована. На вашу электронную почту выслан доступ в личный кабинет.')
                        d = {'user': order.user, 'plain_password': plain_password}

                        template_t = get_template('email/user-registered.txt')
                        message = template_t.render(d)
                        try:
                            send_mail('Регистрация на сайте', message, settings.DEFAULT_FROM_EMAIL, [order.user.email])
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                else:
                    messages.add_message(request, messages.SUCCESS, 'Ваша заявка зарегистрирована')

            order.save()

            d = {'user': order.user, 'order': order}

            if request.user.is_authenticated:
                template_t = get_template('email/user-order-created.txt')
                template_a = get_template('email/adm-order-created.txt')
            else:
                template_t = get_template('email/user-calc-created.txt')
                template_a = get_template('email/adm-calc-created.txt')
            message_t = template_t.render(d)
            message_a = template_a.render(d)
            try:
                send_mail('Заявка на сайте', message_a, settings.DEFAULT_FROM_EMAIL, [settings.NOTIFY_EMAIL])
                send_mail('Оформление заказа на сайте', message_t, settings.DEFAULT_FROM_EMAIL, [order.user.email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.add_message(request, messages.SUCCESS,
                'Ваша заявка на расчет принята и поступила на обработку к нашим менеджерам. Обработка выполняется в '
                    'течении нескольких рабочих часов, по результатам обработки вы получите подробную калькуляцию наших услуг. '
                    'В случае возникновения вопросов менеджер свяжется с вами.')

            return redirect(reverse('orders.created'))
        else:
            if novalidate:
                form._errors = ErrorDict()
                form.full_clean = form._full_clean

    else:
        if request.user.is_authenticated:
            form = CabinetOrderForm()
        else:
            form = OrderFormLt()

    return render(request, 'website/cabinet/orders-create-lt.html', {
        'form':form
    })

@login_required
def order_show(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    return render(request, 'website/cabinet/order-show.html', {
        'order':order
    })

@login_required
def cargo_index(request):
    cargos = Cargo.objects.filter(order__user=request.user).order_by('-id').all()
    paginator = Paginator(cargos, 2)
    page = request.GET.get('p')
    cargos = paginator.get_page(page)

    return render(request, 'website/cabinet/cargo-index.html', {
        'cargos': cargos
    })

def created(request):
    return render(request, 'website/order-created.html', {
    })

def calculator_page(request):
    if request.user.is_authenticated:
        return order_create(request)
    if request.method == "POST":
        form = CalcForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            user = User.register(form.cleaned_data.get('name'), form.cleaned_data.get('email'),
                                       form.cleaned_data.get('phone'))
            if user :
                order.user = user
                order.save()

                messages.add_message(request, messages.SUCCESS,
                                     'Вы зарегистрированы на сайте, письмо с регистрационными данными выслано на ваш адрес')
                messages.add_message(request, messages.SUCCESS,
                    'Ваш ' + str(order) + ' оформлен и поступил на обработку к нашим менеджерам. Обработка выполняется в '
                                     'течении нескольких рабочих часов, по результатам обработки вы получите счет на '
                                     'оплату услуг. В случае возникновения вопросов менеджер свяжется с вами.')

                return redirect(reverse('orders.created'))

            cost = randint(1000,10000)

            return render(request, 'website/calculator-page.html', {
                'cost': cost,
                'form': form
            })
    else:
        form = CalcForm()
    return render(request, 'website/calculator-page.html', {
        'form': form
    })

def cargo_info(request, cargo_code):
    cargo = Cargo.objects.filter(code=cargo_code).first()
    return render(request, 'website/cargo-info.html', {
        'cargo':cargo
    })

@login_required
def cargo_show(request, cargo_id):
    cargo = Cargo.objects.filter(id=cargo_id).first()
    return render(request, 'website/cabinet/cargo-show.html', {
        'cargo':cargo
    })