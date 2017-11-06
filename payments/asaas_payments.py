from django.conf import settings
import requests
import json


def get_headers():
    headers = {
        'Content-Type': 'application/json',
        'access_token': settings.ASAAS_API_KEY
    }
    return headers


def create_payment_boleto(data=None, api_key=''):
    """
    creates new payment
    """
    url = settings.ASAAS_API_URL + '/payments'
    headers = get_headers()
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def create_payment_cc(data=None, api_key=''):
    """
    creates new payment
    """
    url = settings.ASAAS_API_URL + '/payments'
    headers = get_headers()
    if data is not None:
        data['billingType'] = 'CREDIT_CARD'
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def get_payment(payment_id='', api_key=''):
    """
    get existing payment based on payment id
    """
    url = settings.ASAAS_API_URL + '/payments/' + payment_id
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def update_payment(payment_id='', data=None, api_key=''):
    """
    update informations on existing payments based on payment id
    """
    url = settings.ASAAS_API_URL + '/payments/' + payment_id
    headers = get_headers()
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def delete_payment(payment_id='', api_key=''):
    """
    delete existing payment based on payment id
    """
    url = settings.ASAAS_API_URL + '/payments/' + payment_id
    headers = get_headers()
    response = requests.delete(url, data=json.dumps(data), headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def get_all_payments(api_key=''):
    """
    list all payments
    """
    url = settings.ASAAS_API_URL + '/payments/'
    headers = get_headers()
    response = requests.get(url, data=json.dumps(data), headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def get_customer_payments(customer_id='', api_key=''):
    """
    get all payments from a customer based on his customer id
    """
    url = settings.ASAAS_API_URL + '/customers/' + customer_id + '/payments'
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def get_subscription_payments(subscription_id='', api_key=''):
    """
    get all payments from a subscription based on its subscription id
    """
    url = settings.ASAAS_API_URL + '/subscriptions/' + subscription_id + '/payments'
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return {'status_code': response.status_code, 'content': response.content}
