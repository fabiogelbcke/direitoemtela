import requests
import json


def create_customer(data=None, api_key=''):
    """
    creates new customer at Asaas. Data is a json style dictionary with client's data that you wish to save
    """
    url = 'https://www.asaas.com/api/v2/customers'
    headers = {'access_token': api_key}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def get_customer(customer_id='', api_key=''):
    """
    Retrieve already created customer from your account at Asaas.
    """
    url = 'https://www.asaas.com/api/v2/customers/' + customer_id
    headers = {'access_token': api_key}
    response = requests.get(url, headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def update_customer(customer_id='', data=None, api_key=''):
    """
    Update existing customer' information
    """
    url = 'https://www.asaas.com/api/v2/customers/' + customer_id
    headers = {'access_token': api_key}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def delete_customer(customer_id='', api_key=''):
    """
    Delete customer from asaas acount
    """
    url = 'https://www.asaas.com/api/v2/customers/' + customer_id
    headers = {'access_token': api_key}
    response = requests.delete(url, headers=headers)
    return {'status_code': response.status_code, 'content': response.content}


def list_customers(api_key=''):
    """
    List all customers registered in your account
    """
    url = 'https://www.asaas.com/api/v2/customers'
    headers = {'access_token': api_key}
    response = requests.get(url, headers=headers)
    return {'status_code': response.status_code, 'content': response.content}
