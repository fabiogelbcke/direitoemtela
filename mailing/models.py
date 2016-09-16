from django.db import models
from django.utils import timezone

# Create your models here.

class MailingEmail(models.Model):
    id = models.AutoField(pk=True)
    email = models.EmailField()
    date_added = models.DateTimeField(default=timezone.now)
