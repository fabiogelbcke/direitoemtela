# -*- coding: utf-8 -*-
from .models import MailingEmail
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.validators import validate_email


def add_to_list(request):
    email = request.POST.get('email', None)
    if email:
        try:
            validate_email(email)
        except:
            return HttpResponseBadRequest('Por favor digite um email válido')
        MailingEmail.objects.create(email=email)
        return HttpResponse('Email Adicionado')
    else:
        return HttpResponseBadRequest('Por favor digite um email válido')
