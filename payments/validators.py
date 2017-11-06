# -*- coding: utf-8 -*-
import re
from django.core.exceptions import ValidationError


def validate_cpf(cpf, d1=0, d2=0, i=0):
    """
    checks if the input cpf is a valid brazilian cpf (brazilian SSN)
    """
    if len(cpf) != 11:
        print 'oi'
        raise ValidationError('CPF deve ter 11 numeros')
    while i < 10:
        d1, d2, i = (d1 + (int(cpf[i]) * (11 - i - 1))
                     ) % 11 if i < 9 else d1, (d2 + (int(cpf[i]) * (11 - i))) % 11, i + 1
    if (int(cpf[9]) == (11 - d1 if d1 > 1 else 0)) and (int(cpf[10]) == (11 - d2 if d2 > 1 else 0)):
        return True
    else:
        raise ValidationError('CPF inválido')


def validate_phone(phone):
    if re.match('^[1-9]{2}[2-9][0-9]{7,8}$', phone):
        return True
    return False

def validate_cvv(cvv):
    return (cvv.isdigit() and (len(cvv) == 3 or len(cvv) == 4))

def validate_expiration_month(expiration_date):
    if re.match('^[0-1][0-9]$', expiration_date):
        return True
    raise ValidationError('Mês de validade deve ser no formato MM')

def validate_expiration_year(expiration_date):
    if re.match('^20[1-2][0-9]$', expiration_date):
        return True
    raise ValidationError('Ano de validade deve ser no formato AAAA')

def validate_cc(cc_number):
    if cc_number.isdigit() is False:
        raise ValidationError('Código de segurança deve ser um número')
