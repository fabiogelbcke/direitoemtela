 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import MyUser
from .forms import UserForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login


def verify_pwd(pwd):
    if pwd is None:
        return False
    if len(pwd) < 8:
        return False
    if (any(x.isalpha() for x in pwd)
        and any(x.isdigit() for x in pwd)):
        return True
    else:
        return False

def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        password = request.POST.get('password', '')
        password_confirmation = request.POST.get('password_confirmation', '')
        if (password != password_confirmation):
            return HttpResponseBadRequest('A senha e a confirmação não batem!')
        if verify_pwd(password) is False:
            return HttpResponseBadRequest(
                'A senha deve ter ao menos 8 caracteres, '
                'entre eles uma letra e um número!'
            )
        user.username = user.email
        user.set_password(password)
        user.save()
        user = authenticate(username=user.email,
                            password=password)
        login(request, user)
        return HttpResponse('Registrado!')
    else:
        print form.errors
        return HttpResponseBadRequest(
            'Não foi possivel concluir o seu registro. '
            'Verifique seus dados e tente novamente.'
        )
        
