# -*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse, HttpResponseBadRequest

from urllib import quote_plus

def logout_function(request):
    logout(request)
    if request.GET.get('next', None):
        return redirect(request.GET.get('next'))
    return redirect('/')
    

def email_login(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        next_page = request.GET.get('next', 'index')
        return redirect(next_page)
    else:
        referer = request.META.get('HTTP_REFERER', 'index')
        response = redirect(referer)
        error_msg = 'Email ou senha incorretos. Tente novamente.'
        response['Location'] += '?login_error=' + quote_plus(error_msg)
        return response


def send_password_reset_email(request):
    pw_form = PasswordResetForm(request.POST)
    if pw_form.is_valid():
        pw_form.save(
            subject_template_name='email-reset-password-subject.txt',
            email_template_name='empty.html',
            html_email_template_name='email-reset-password.djhtml',
            request=request
        )
        return HttpResponse('email sent')
    return HttpResponseBadResponse(
        'Email Inválido'
    )
