from django.db import models
from django.utils import timezone

# Create your models here.

class MailingEmail(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    date_added = models.DateTimeField(default=timezone.now)
