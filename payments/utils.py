# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen
from django.http import HttpResponseBadRequest
from .forms import BillingInfoForm, CreditCardForm
from django.utils import timezone
from django.conf import settings


def get_payment_json(user, card_data, course, payment):
    billing_info = user.billing_info
    month = card_data['expiration_date'].split('/')[0]
    year = card_data['expiration_date'].split('/')[1]
    now = timezone.now()
    values =
    {
        "customer": billing_info.asaas_id,
        "billingType": "CREDIT_CARD",
        "dueDate": str(now.year) + '-' + str(now.month) + '-' + str(now.day),
        "value": course.price,
        "description": course.name,
        "externalReference": str(payment.id),
        "creditCard": {
            "holderName": ['card_name'],
            "number": ['cc_number'],
            "expiryMonth": month,
            "expiryYear": year,
            "ccv": card_data['cvv']
        },
        "creditCardHolderInfo": {
            "name": ['card_name'],
            "email": user.email,
            "cpfCnpj": billing_info.cpf,
            "postalCode": billing_info.postal_code,
            "addressNumber": billing_info.address_no,
            "addressComplement": billing_info.address,
            "mobilePhone": billing_info.phone
        }
    }
    return str(values)
    

def get_customer_json(user, cours):
    if hasattr(user, 'billing_info') is False:
        return None
    billing_info = user.billing_info
    values =
    {
        "name": , user.get_full_name()
        "email": user.email
        "mobilePhone": billing_info.phone,
        "cpfCnpj": billing_info.cpf,
        "postalCode": billing_info.postal_code,
        "address": billing_info.address,
        "addressNumber": billing_info.address_no,
        "externalReference": str(user.id),
    }
    return str(values)

def get_headers():
    headers = {
        'Content-Type': 'application/json',
        'access_token': settings.ASAAS_API_KEY
    }
    return headers
request = Request('https://www.asaas.com/api/v3/payments', data=values, headers=headers)

response_body = urlopen(request).read()
print response_body

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

    
def make_card_payment(request):
    user = request.user
    if update_billing_info(request, user) is False:
        return HttpResponseBadRequest(
            'Houve um problema. Verifique seu telefone e '
            'cpf e tente novamente.'
        )
    cc_form = CreditCardForm(request.POST)
    if cc_form.is_valid():
        card_data = cc_form.cleaned_data()
        get_payment_json(user, card_data)
