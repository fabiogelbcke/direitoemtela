from __future__ import unicode_literals
import os
import magic
from django.core.exceptions import ValidationError
from django.db import models
import uuid
from django.conf import settings

# Create your models here.

def validate_reading_extension(reading_file):
    ext = os.path.splitext(reading_file.name)[-1]
    valid_extensions = settings.READING_VALID_EXTENSIONS
    if not ext in valid_extensions:
        error_msg = (
            'Invalid file format. Please upload a file with one of the allowed formats.')
        raise ValidationError(error_msg, code='invalid')

def validate_reading_format(reading_file):
    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        mime_type = m.id_buffer(reading_file.file.read(1024))
        reading_file.file.seek(0)
    if mime_type not in settings.READING_VALID_TYPES:
        raise ValidationError(
            ('Invalid file format. Please upload a file with one of the allowed formats.'))

def get_reading_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('readings', str(instance.id), filename)

class Reading(models.Model):
    id = models.AutoField(primary_key=True)
    reading_file = models.FileField(upload_to=get_reading_path,
                                default='',
                                blank=True,
                                validators=[validate_reading_format,]
                                )
    description = models.TextField(blank=True,
                                   default='')
    title = models.CharField(blank=True,
                            default='',
                            max_length=100)
    
