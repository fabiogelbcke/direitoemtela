 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import loader

import requests

from .models import MyUser
from .forms import UserForm
from .validators import validate_password


def send_registration_email(email):
    template = loader.get_template('email-mailing-list.html')
    content = template.render({})
    subject = 'Direito em Tela - Obrigado por se cadastrar!'
    msg = EmailMultiAlternatives(subject=subject,
                                 from_email='Equipe Direito em Tela <contato@direitoemtela.com.br>',
                                 to=[email,])
    msg.attach_alternative(content, 'text/html')
    msg.send()


def add_to_mailchimp(user):
    url = (
        'https://us16.api.mailchimp.com/3.0/lists/'
        + settings.MAILCHIMP_USER_LIST_ID + '/members/'
    )
    json_data = (
        '{"email_address": "'
        + user.email
        +'","status": "subscribed","merge_fields":{"FNAME": "'
        + user.first_name
        + '","LNAME": "'
        + user.last_name
        + '"}}').encode('utf-8'
        )
    r = requests.post(
        url,
        auth=(
            'ILoveBlowjobs',
            settings.MAILCHIMP_API_KEY
        ),
        data=json_data
    )
    return r


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
        send_registration_email(user.email)
        add_to_mailchimp(user)
        next_page_url = request.GET.get('next', '/')
        next_page_url = settings.WEBSITE_URL[:-1] + next_page_url
        return HttpResponse(next_page_url)
    else:
        return HttpResponseBadRequest(
            'Não foi possivel concluir o seu registro. '
            'Verifique seus dados e tente novamente.'
        )
        
