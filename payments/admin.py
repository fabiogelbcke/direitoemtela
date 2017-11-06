# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import PromoCode


class PromoCodeAdmin(admin.ModelAdmin):
    model = PromoCode
    list_display = ('code', 'used', 'used_by', 'date_used')


admin.site.register(PromoCode, PromoCodeAdmin)

# Register your models here.
