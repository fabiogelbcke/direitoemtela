from django.conf import settings
from django.contrib.staticfiles.storage import CachedFilesMixin
from storages.backends.s3boto import S3BotoStorage, S3Connection
from django.core.files.storage import get_storage_class
import copy


class BRConnection(S3Connection):
    DefaultHost = 's3-sa-east-1.amazonaws.com'


class StaticStorage(S3BotoStorage):
    connection_class = BRConnection
    location = settings.STATICFILES_LOCATION
    def __init__(self, *args, **kwargs):
        super(StaticStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        non_gzipped_file_content = content.file
        name = super(StaticStorage, self).save(name, content)
        content.file = non_gzipped_file_content
        self.local_storage._save(name, content)
        return name
    


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
