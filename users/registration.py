 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.urls import reverse

from .models import MyUser
from .forms import UserForm
from .validators import validate_password


def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        password = request.POST.get('password', '')
        password_confirmation = request.POST.get('password_confirmation', '')
        if (password != password_confirmation):
            return HttpResponseBadRequest('A senha e a confirmação não batem!')
        if validate_password(password) is False:
            return HttpResponseBadRequest(
                'A sua senha deve ter ao menos 8 caracteres!'
            )
        user.username = user.email
        user.set_password(password)
        user.save()
        user = authenticate(username=user.email,
                            password=password)
        login(request, user)
        next_page_url = request.GET.get('next', '/')
        next_page_url = settings.WEBSITE_URL[:-1] + next_page_url
        return HttpResponse(next_page_url)
    else:
        return HttpResponseBadRequest(
            'Não foi possivel concluir o seu registro. '
            'Verifique seus dados e tente novamente.'
        )
        
