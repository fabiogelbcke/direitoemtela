from django.contrib import admin
from .models import MailingEmail
# Register your models here.

class MailingEmailAdmin(admin.ModelAdmin):
    list_display=('email', 'date_added')

admin.site.register(MailingEmail, MailingEmailAdmin)
