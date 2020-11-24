import datetime

AWS_GROUPNAME="Chadolskii_ecomm_group"
AWS_USERNAME = "chadolskii-ecomm-user"

AWS_ACCESS_KEY_ID = "AKIA2WVZDJELZWFVYXV3"
AWS_SECRET_ACCESS_KEY = "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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'ecomm.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'ecomm.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'chadoslkii-ecomm'

AWS_S3_REGION_NAME = "ap-northeast-2"
AWS_S3_SIGNATURE_VERSION = "s3v4"


S3DIRECT_REGION = 'ap-northeast-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'





two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()),),
}

PROTECTED_DIR_NAME = 'protected'
PROTECTED_MEDIA_URL = 's3//%s/%s/' %( AWS_STORAGE_BUCKET_NAME, PROTECTED_DIR_NAME)

# https://chadolskii-ecomm.s3.us-west-2.amazonaws.com/protected/

AWS_DOWNLOAD_EXPIRE = 5000 #(0ptional, in milliseconds)