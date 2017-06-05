# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from urllib2 import Request, urlopen
from urllib import quote_plus
from .forms import BillingInfoForm, CreditCardForm
from .models import Payment, BillingInfo, CreditCard
from datetime import timedelta
import json
from courses.models import Course
from courses.utils import register_to_course


def get_payment_json(user, card_data, payment, ip_addr):
    billing_info = user.billing_info
    tomorrow = timezone.now() + timedelta(days=1)
    values = {
        "customer": billing_info.asaas_id,
        "billingType": "CREDIT_CARD",
        "dueDate": (str(tomorrow.year) + '-'
                    + str(tomorrow.month).zfill(2) + '-'
                    + str(tomorrow.day).zfill(2)),
        "value": int(payment.amount),
        "description": payment.description,
        "externalReference": str(payment.id),
        "creditCard": {
            "holderName": card_data['card_name'],
            "number": card_data['cc_number'],
            "expiryMonth": card_data['expiration_month'],
            "expiryYear": card_data['expiration_year'],
            "ccv": card_data['cvv']
        },
        "creditCardHolderInfo": {
            "name": card_data['card_name'],
            "email": user.email,
            "cpfCnpj": billing_info.cpf,
            "postalCode": billing_info.postal_code,
            "addressNumber": billing_info.address_no,
            "addressComplement": billing_info.address,
            "mobilePhone": billing_info.phone,
            "remoteIp": ip_addr
        }
    }
    return json.dumps(values)
    

def get_customer_json(user):
    if hasattr(user, 'billing_info') is False:
        return None
    billing_info = user.billing_info
    values = {
        "name": user.get_full_name(),
        "email": user.email,
        "mobilePhone": billing_info.phone,
        "cpfCnpj": billing_info.cpf,
        "postalCode": billing_info.postal_code,
        "address": billing_info.address,
        "addressNumber": billing_info.address_no,
        "externalReference": str(user.id),
    }
    print json.dumps(values)
    return json.dumps(values)

def get_headers():
    headers = {
        'Content-Type': 'application/json',
        'access_token': settings.ASAAS_API_KEY
    }
    return headers


def update_billing_info(request, user):
    if hasattr(user, 'billing_info'):
        instance = user.billing_info
    else:
        instance = BillingInfo.objects.create(user=user)
    form = BillingInfoForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        return True
    else:
        return False


def create_asaas_user(user):
    values = get_customer_json(user)
    request = Request(
        settings.ASAAS_API_URL + '/customers',
        data=values,
        headers=get_headers()
    )
    try:
        response = urlopen(request)
        print response
        response_body = json.loads(response.read())
    except Exception as e:
        print e
        return None
    billing_info = user.billing_info
    billing_info.asaas_id = response_body['id']
    billing_info.save()
    return billing_info.asaas_id
    

def make_card_payment(card_data, user, course, ip_addr):
    payment = Payment.objects.create(
        user=user,
        amount=course.price,
        description=course.name
    )
    values = get_payment_json(
        user,
        card_data,
        payment,
        ip_addr
    )
    print values
    request = Request(
        settings.ASAAS_API_URL + '/payments',
        data=values,
        headers=get_headers()
    )
    try:
        response = urlopen(request)
        print response
        response_body = json.loads(response.read())
        print response_body
        if response_body['status'] == 'CONFIRMED':
            card_info = response_body['creditCard']
            card = CreditCard.objects.get_or_create(
                user=user,
                brand=card_info['creditCardBrand'],
                last_four=card_info['creditCardNumber'],
            )[0]
            #asaas_token = card_info['creditCardToken']
            payment.credit_card = card
            payment.done = True
            payment.save()
            return True
        else:
            return False
    except Exception as e:
        print e
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def make_course_payment(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)
    ip_addr = get_client_ip(request)
    if update_billing_info(request, user) is False:
        return HttpResponseBadRequest(
            'Houve um problema. Verifique seu telefone e '
            'cpf e tente novamente.'
        )
    if not user.billing_info.asaas_id:
        customer_id = create_asaas_user(user)
        if customer_id is None:
            return HttpResponseBadRequest(
                'Houve um problema. Verifique seus dados e '
                'tente novamente.'
            )
    cc_form = CreditCardForm(request.POST)
    if not cc_form.is_valid():
        response = redirect('course_page', course_id=course_id)
        error_msg =  ('Dados do cartão inválidos.')
        response['Location'] += '?error_msg=' + quote_plus(error_msg)
        return response
    card_data = cc_form.cleaned_data
    payment_worked = make_card_payment(
        card_data,
        user,
        course,
        ip_addr
    )
    if payment_worked is False:
        response = redirect('course_page', slug=course_id)
        error_msg =  ('Não foi possível realizar a cobrança. Cheque '
                      'os dados e tente novamente.')
        response['Location'] += '?error_msg=' + quote_plus(error_msg)
        return response
    register_to_course(user.id, course.id)
    return redirect('course_progress', course_id=course_id)