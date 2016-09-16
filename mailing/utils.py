from .models import MailingEmail
from django.http import HttpResponse, HttpResponseBadRequest


def add_to_list(request):
    email = request.POST.get('email', None)
    if email:
        MailingEmail.objects.create(email=email)
        return HttpResponse('Email Adicionado')
    else:
        return HttpResponseBadRequest('Por favor digite um email válido')
