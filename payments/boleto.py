# -*- coding: utf-8 -*-
from .asaas_payments import create_payment_boleto
from .forms import BillingInfoForm
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import logging

from urllib2 import Request, urlopen
from urllib import quote_plus
from datetime import timedelta
import json

from courses.models import Course
from courses.utils import register_to_course

from .models import Payment, BillingInfo, PromoCode
from .forms import CPFForm
from .utils import (create_asaas_user, get_client_ip,
                    calculate_price_with_promo_code,
                    check_promo_code_validity)

logger = logging.getLogger(__name__)

def send_boleto_email(boleto_url, user, course):
    template = loader.get_template('email-boleto.djhtml')
    content = template.render({
        'boleto_url': boleto_url,
        'user': user,
        'course': course
    })
    subject = 'Boleto ' + course.name
    email = user.email
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email='Equipe Direito em Tela <contato@direitoemtela.com.br>',
        to=[email,]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send()
    return True


def update_cpf(request, user):
    if hasattr(user, 'billing_info'):
        instance = user.billing_info
    else:
        instance = BillingInfo.objects.create(user=user)
    form = CPFForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        return True
    else:
        return False

def get_boleto_json(user, payment, ip_addr):
    billing_info = user.billing_info
    deadline = timezone.now() + timedelta(days=3)
    values = {
        "customer": billing_info.asaas_id,
        "billingType": "BOLETO",
        "dueDate": (str(deadline.year) + '-'
                    + str(deadline.month).zfill(2) + '-'
                    + str(deadline.day).zfill(2)),
        "value": str(payment.amount),
        "description": payment.description,
        "externalReference": str(payment.id),
    }
    return values

        
@login_required
def generate_boleto(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)
    code = request.POST.get('code', '')
    if code:
        code_valid, error_msg = check_promo_code_validity(code, course)
        if code_valid is False:
            return HttpResponseBadRequest(error_msg)
        promo_code_obj = PromoCode.objects.filter(
            code=code,
            used=False
        ).first()
        price = calculate_price_with_promo_code(promo_code_obj, course)
    else:
        price = course.price
    payment = Payment.objects.create(
        user=user,
        amount=price,
        description=course.name,
        billing_type='BOLETO',
        course=course
    )
    #updating the CPF in BillingInfo instance
    if update_cpf(request, user) is False:
        return HttpResponseBadRequest(
            'CPF Inválido. Certifique-se de que o CPF está '
            'correto e de que você está digitando apenas números'
        )
    if not user.billing_info.asaas_id:
        asaas_id = create_asaas_user(user)
    else:
        asaas_id = user.billing_info.asaas_id
    if asaas_id is None:
        return HttpResponseBadRequest(
            'Nosso provedor de pagamento não está '
            'respondendo. Por favor, tente novamente '
            'em alguns minutos.'
        )
    ip_addr = get_client_ip(request)
    data = get_boleto_json(
        user,
        payment,
        ip_addr
    )
    response = create_payment_boleto(
        data,
        settings.ASAAS_API_KEY
    )
    if response['status_code'] != 200:
        return HttpResponseBadRequest(
            'Houve um erro na hora de criar o pagamento. '
            'Verifique se os dados que você digitou estão '
            'corretos e tente novamente.'
        )
    boleto_url = json.loads(response['content'])['bankSlipUrl']
    send_boleto_email(boleto_url, user, course)
    return HttpResponse(boleto_url)
    #process response, get boleto url and return it


def send_payment_confirmation_email(user, course):
    template = loader.get_template('email-payment-confirmation.djhtml')
    content = template.render({
        'website_url': settings.WEBSITE_URL[:-1],
        'user': user,
        'course': course
    })
    subject = 'Pagamento confirmado!'
    email = user.email
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email='Equipe Direito em Tela <contato@direitoemtela.com.br>',
        to=[email,]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send()
    return True


@csrf_exempt
def payment_update(request):
    request_json = json.loads(request.body)
    if request_json['event'] == 'PAYMENT_RECEIVED':
        payment_id = int(request_json['payment']['externalReference'])
        payment = Payment.objects.get(id=payment_id)
        payment.done = True
        payment.save()
        course = payment.course
        user = payment.user
        register_to_course(user.id, course.id)
        send_payment_confirmation_email(user, course)
        return HttpResponse('Payment Processed')
    return HttpResponse('Something else')


def send_course_completed_email(course_rel, user):
    course = course_rel.course
    if course_rel.passed == True:
        template = loader.get_template('email-course-passed.djhtml')
    else:
        template = loader.get_template('email-course-failed.djhtml')
    content = template.render({
        'boleto_url': boleto_url,
        'user': user,
        'course': course
    })
    subject = 'Curso de ' + course.name + ' Completo!'
    email = user.email
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email='Equipe Direito em Tela <contato@direitoemtela.com.br>',
        to=[email,]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send()
    return True


def complete_course(course_rel, user):
    course_rel.passed = course_rel.percentage() >= course_rel.passing_grade
    course_rel.completed = True
    course_rel.completion_date = timezone.now()
    course_rel.certificate = create_certificate(course_rel)
    course_rel.save()
    user.course_hours += course.hours
    user.save()
    send_course_completed_email(course_rel.course, user)
    return course_rel
