from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import login
from .models import User
from django.conf import settings
from website.models import Contact
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required

def register(request):
    pass
    if request.method != "POST":
        form = RegisterForm()
        return render(request, 'website/register.html', {
            'form': form,
            'message': ''
        })
    form = RegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'website/register.html', {
            'form': form,
            'message' : ''
        })
    plain_password = form.cleaned_data.get('password')
    user = User.objects.create_user(**form.cleaned_data)
    user.set_password(plain_password)
    user.save()
    d = {'user': user, 'plain_password': plain_password}
    template_t = get_template('email/adm-registered.txt')
    message = template_t.render(d)
    try:
        send_mail('Регистрация на сайте', message, settings.DEFAULT_FROM_EMAIL, [settings.NOTIFY_EMAIL])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    template_t = get_template('email/user-registered.txt')
    message = template_t.render(d)
    try:
        send_mail('Регистрация на сайте', message, settings.DEFAULT_FROM_EMAIL, [user.email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    login(request, user)
    return redirect('/')


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method != 'POST':
        return render(request, 'website/cabinet/profile.html', {
            'form':form
        })
    if not form.is_valid():
        return render(request, 'website/cabinet/profile.html', {
            'form':form
        })
    form.save()
    return redirect(reverse('user.profile'))
