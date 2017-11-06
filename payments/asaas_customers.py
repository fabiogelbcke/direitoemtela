from django.conf import settings
import requests
import json


def get_headers():
    headers = {
        'Content-Type': 'application/json',
        'access_token': settings.ASAAS_API_KEY
    }
    return headers


def create_customer(data=None, api_key=''):
    """
    creates new customer at Asaas. Data is a json style dictionary with client's data that you wish to save
    """
    url = settings.ASAAS_API_URL + '/customers'
    headers = get_headers()
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def get_customer(customer_id='', api_key=''):
    """
    Retrieve already created customer from your account at Asaas.
    """
    url = settings.ASAAS_API_URL + '/customers/' + customer_id
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def update_customer(customer_id='', data=None, api_key=''):
    """
    Update existing customer' information
    """
    url = settings.ASAAS_API_URL + '/customers/' + customer_id
    headers = get_headers()
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def delete_customer(customer_id='', api_key=''):
    """
    Delete customer from asaas acount
    """
    url = settings.ASAAS_API_URL + '/customers/' + customer_id
    headers = get_headers()
    response = requests.delete(url, headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def list_customers(api_key=''):
    """
    List all customers registered in your account
    """
    url = settings.ASAAS_API_URL + '/customers'
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return {'status_code': response.status_code, 'content': response.content}
