import keys

AWS_STORAGE_BUCKET_NAME = keys.S3_BUCKET_NAME
AWS_CLOUDFRONT_DOMAIN = 'd19z6v2bmduc4j.cloudfront.net'
AWS_ACCESS_KEY_ID = keys.S3_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = keys.S3_SECRET_KEY

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_CLOUDFRONT_DOMAIN, STATICFILES_LOCATION)

COMPRESS_URL = STATIC_URL

COMPRESS_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_CLOUDFRONT_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

DEBUG = False

ALLOWED_HOSTS = ['direitoemtela.com.br', 'www.direitoemtela.com.br', '52.67.110.163']

WEBSITE_URL = 'https://www.direitoemtela.com.br/'


#CACHES = {
#    'default': {
#        'BACKEND': 'redis_cache.RedisCache',
#        'LOCATION': 'gigloopredis.80k2su.0001.sae1.cache.amazonaws.com:6379',
#    }
#}
