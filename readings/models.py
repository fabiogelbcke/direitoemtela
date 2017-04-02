from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Reading(models.Model):
    pdf_file = models.FileField()
    description = models.TextField(blank=True,
                                   default='')
    
