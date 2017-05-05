import re


def validate_cpf(cpf, d1=0, d2=0, i=0):
    """
    checks if the input cpf is a valid brazilian cpf (brazilian SSN)
    """
    while i < 10:
        d1, d2, i = (d1 + (int(cpf[i]) * (11 - i - 1))
                     ) % 11 if i < 9 else d1, (d2 + (int(cpf[i]) * (11 - i))) % 11, i + 1
    if (int(cpf[9]) == (11 - d1 if d1 > 1 else 0)) and (int(cpf[10]) == (11 - d2 if d2 > 1 else 0)):
        return True
    else:
        return False


def validate_phone(phone):
    if re.match('^[1-9]{2}[2-9][0-9]{7,8}$', phone):
        return True
    return False

def validate_cvv(cvv):
    return (cvv.isdigit() and (len(cvv) == 3 or len(cvv) == 4))

def validate_expiration_month(expiration_date):
    if re.match('^[0-1][0-9]$', expiration_date):
        return True
    return False

def validate_expiration_year(expiration_date):
    if re.match('^20[1-2][0-9]$', expiration_date):
        return True
    return False

def validate_cc(cc_number):
    return cc_number.isdigit()
