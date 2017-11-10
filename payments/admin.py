# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import PromoCode, Payment


class PromoCodeAdmin(admin.ModelAdmin):
    model = PromoCode
    list_display = ('code', 'used', 'used_by', 'date_used')

class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ('id', 'user', 'course', 'amount', 'done', 'billing_type')


admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(Payment, PaymentAdmin)

# Register your models here.
