# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings

from random import randint
import shortuuid

from users.models import MyUser
from courses.models import Course
# Create your models here.

def random_address_number():
    return str(randint(1,200))

def create_promo_code():
    shortuuid.set_alphabet("abcdefghijklmnopqrstuvwxyz0123456789")
    return shortuuid.uuid()[:12]

class BillingInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='billing_info',
                                null=True,
                                default=None)
    cpf = models.CharField(max_length=20)
    phone = models.CharField(max_length=20,
                             default='',
                             blank=True)
    address_no = models.CharField(max_length=6,
                                  default='',
                                  blank=True)
    address = models.TextField(blank=True,
                               default='')
    postal_code = models.CharField(max_length=15,
                                   default='',
                                   blank=True)
    asaas_id = models.CharField(max_length=30,
                                blank=True,
                                default='')
    

class CreditCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True,
                             default=None,
                             related_name='credit_cards')
    brand = models.CharField(max_length=20)
    last_four = models.CharField(max_length=4)
    asaas_token = models.CharField(max_length=80,
                                   blank=True,
                                   default='')


class Payment(models.Model):
    id = models.AutoField(primary_key=True)

    COURSE = 'C'
    SLIDES = 'S'
    ITEM_TYPE_CHOICES = (
        (COURSE, 'Course'),
        (SLIDES, 'Slide Collection')
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True,
                             default=None,
                             related_name='payments')
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=6
    )
    billing_type = models.CharField(
        max_length=20,
        default='CREDIT_CARD'
    )
    done = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    description = models.CharField(
        max_length=80,
        blank=True,
        default=''
    )
    credit_card = models.ForeignKey(
        CreditCard,
        null=True,
        default=None,
        blank=True
    )
    course = models.ForeignKey(
        Course,
        null=True,
        default=None
    )
    item_name = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    item_type = models.CharField(
        max_length=30,
        choices=ITEM_TYPE_CHOICES,
        default=COURSE
    )
                                 
                                 


class PromoCode(models.Model):
    code = models.CharField(max_length=30,
                            default=create_promo_code,
                            unique=True)
    used = models.BooleanField(default=False)
    used_by = models.ForeignKey(MyUser,
                                blank=True,
                                null=True,
                                default=None)
    one_time_use = models.BooleanField(default=True)
    date_used = models.DateTimeField(default=None,
                                     blank=True,
                                     null=True)
    percentage = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5,
                                   decimal_places=2,
                                   default=100)
    course = models.ForeignKey(Course,
                               default=None,
                               null=True,
                               blank=True)
