# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from random import randint

# Create your models here.

def random_address_number():
    return str(randint(1,200))

class BillingInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='billing_info')
    cpf = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address_no = models.CharField(max_length=6)
    address = models.TextField(blank=True, default='')
    postal_code = models.CharField(max_length=15)
    asaas_id = models.CharField(max_length=30,
                                blank=True,
                                default='')
    

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='payments')
    amount = models.DecimalField(decimal_places=2,
                                 max_digits=6)
    billing_type = models.CharField(max_length=20,
                                    default='CREDIT_CARD')
    done = models.BooleanField(default=False)
    description = models.CharField(max_length=80)


class CreditCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='credit_cards')
    moip_id = models.CharField(max_length=30)
    brand = models.CharField(max_length=20)
    first_six = models.CharField(max_length=6)
    last_four = models.CharField(max_length=4)
    card_name = models.CharField(max_length=40)
