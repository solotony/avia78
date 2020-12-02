from django.shortcuts import render, redirect, reverse
from .forms import MessageFromSite, MessageFromCabinet, DocQueryFromSite, DocQueryFromCabinet
from myuser.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.loader import get_template
from .models import Message
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings

@login_required
def cabinet_index(request):
    msgs = Message.objects.filter(user=request.user).order_by('-id').all()
    paginator = Paginator(msgs, 2)
    page = request.GET.get('p')
    msgs = paginator.get_page(page)

    return render(request, 'website/cabinet/messages-index.html', {
        'msgs':msgs
    })

def create(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = MessageFromCabinet(request.POST)
        else:
            form = MessageFromSite(request.POST)

        if form.is_valid():

            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
                msg.email = request.user.email
                msg.phone = request.user.phone
                msg.name = request.user.first_name + ' ' + request.user.last_name
            else:
                if form.cleaned_data.get('register'):
                    password = '1qazxsws!@F'
                    msg.user = User.register(msg.name, msg.email, msg.phone, plain_password=password)
                    if not msg.user:
                        messages.add_message(request, messages.ERROR,
                            'Регистрация не удалась, возможно пользователь с таким e-mail уже зарегистрирован')
                    else:
                        d = {'user': msg.user, 'plain_password':password}
                        template_t = get_template('email/user-registered.txt')
                        message_t = template_t.render(d)
                        try:
                            send_mail('Регистрация на сайте', message_t, settings.DEFAULT_FROM_EMAIL,
                                      ['as@solotony.com', settings.NOTIFY_EMAIL])
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')

                        messages.add_message(request, messages.SUCCESS,
                            'Вы зарегистрированы на сайте, письмо с регистрационными данными выслано на ваш адрес')
            msg.status = Message.STATUS_SEND
            msg.type = Message.TYPE_QUESTION
            msg.title = 'Вопрос с сайта'
            msg.save()

            messages.add_message(request, messages.SUCCESS, 'Ваш вопрос отправлен, ожидайте ответа')

            d = {'msg': msg }
            template_t = get_template('email/message-from-site.txt')
            message_t = template_t.render(d)

            try:
                send_mail('Вопрос с сайта', message_t, settings.DEFAULT_FROM_EMAIL, ['as@solotony.com', settings.NOTIFY_EMAIL])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return redirect(reverse('messages.created'))
    else:
        if request.user.is_authenticated:
            form = MessageFromCabinet()
        else:
            form = MessageFromSite()

    return render(request, 'website/message-create.html', {
        'form':form
    })

def create_doc(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = DocQueryFromCabinet(request.POST)
        else:
            form = DocQueryFromSite(request.POST)

        if form.is_valid():

            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            else:
                if form.cleaned_data.get('register'):
                    password = '1qazxsws!@F'
                    msg.user = User.register(msg.name, msg.email, msg.phone, plain_password=password)
                    if not msg.user:
                        messages.add_message(request, messages.ERROR,
                            'Регистрация не удалась, возможно пользователь с таким e-mail уже зарегистрирован')
                    else:

                        d = {'user': msg.user, 'plain_password':password}
                        template_t = get_template('email/user-registered.txt')
                        message_t = template_t.render(d)
                        try:
                            send_mail('Регистрация на сайте', message_t, settings.DEFAULT_FROM_EMAIL,
                                      ['as@solotony.com', settings.NOTIFY_EMAIL])
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')


                        messages.add_message(request, messages.SUCCESS,
                            'Вы зарегистрированы на сайте, письмо с регистрационными данными выслано на ваш адрес')
            msg.status = Message.STATUS_SEND
            msg.type = Message.TYPE_DOC_REQUEST
            msg.title = 'Запрос на документы по заказу ' +  form.cleaned_data.get('order_id')
            msg.save()

            messages.add_message(request, messages.SUCCESS, 'Запрос на документы отправлен отправлен, ожидайте ответа')
            return redirect(reverse('messages.created'))
    else:
        if request.user.is_authenticated:
            form = DocQueryFromCabinet()
        else:
            form = DocQueryFromSite()

    return render(request, 'website/message-create-doc.html', {
        'form':form
    })

def create_query(request):
    return render(request, 'website/message-create-query.html', {
    })

def created(request):
    return render(request, 'website/message-created.html', {
    })

@login_required
def cabinet_message(request, message_id):
    return render(request, 'website/cabinet/messages-edit.html', {
        'message_id':message_id
    })

@login_required
def cabinet_create(request):
    return create(request)