# -*- coding: utf-8 -*-
from .models import MailingEmail
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.validators import validate_email
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import RequestContext, loader, Context

def add_to_list(request):
    email = request.POST.get('email', None)
    if email:
        try:
            validate_email(email)
        except:
            return HttpResponseBadRequest('Por favor digite um email válido')
        if not MailingEmail.objects.filter(email=email).exists():
            MailingEmail.objects.create(email=email)
        template = loader.get_template('email-mailing-list.html')
        content = template.render(Context({}))
        subject = 'Direito em Tela - Obrigado por se cadastrar!'
        msg = EmailMultiAlternatives(subject=subject,
                                     from_email='Equipe Direito em Tela <contato@direitoemtela.com.br>',
                                     to=[email,])
        msg.attach_alternative(content, 'text/html')
        msg.send()
        print 'aew'
        return HttpResponse('Email Adicionado')
    else:
        return HttpResponseBadRequest('Por favor digite um email válido')
