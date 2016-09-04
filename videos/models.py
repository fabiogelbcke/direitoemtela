from django.db import models


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
# Create your models here.
