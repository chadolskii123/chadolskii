# aws.download.utils.py


import boto3
import re
import os

from django.conf import settings


class AWSDownload(object):
    access_key = None
    secret_key = None
    bucket = None
    region = None
    expires = getattr(settings, 'AWS_DOWNLOAD_EXPIRE', 5000)

    def __init__(self, access_key, secret_key, bucket, region, *args, **kwargs):
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        super(AWSDownload, self).__init__(*args, **kwargs)

    def s3connect(self):
        s3 = boto3.resource(
            service_name='s3',

            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )
        for bucket in s3.buckets.all() :
            print(bucket.name)
            if bucket.name == 'chadoslkii-ecomm':
                return bucket
        return None

        # conn = boto.connect_s3(
        #     #region=self.region,
        #     aws_access_key_id=self.access_key,
        #     aws_secret_access_key=self.secret_key,
        #     is_secure=True,
        #     calling_format=OrdinaryCallingFormat()
        # )
        # return conn

    def get_bucket(self):
        conn = self.s3connect()
        # bucket_name = self.bucket
        # bucket = conn.get_bucket(bucket_name, validate=False)
        return conn #bucket

    def get_key(self, path):
        bucket = self.get_bucket()
        key = bucket.get_key(path)
        return key

    def get_filename(self, path, new_filename=None):
        current_filename = os.path.basename(path)
        if new_filename is not None:
            filename, file_extension = os.path.splitext(current_filename)
            escaped_new_filename_base = re.sub(
                '[^A-Za-z0-9\#]+',
                '-',
                new_filename)
            escaped_filename = escaped_new_filename_base + file_extension
            return escaped_filename
        return current_filename

    def generate_url(self, path, download=True, new_filename=None):
        file_url = None
        aws_obj_key = self.get_key(path)
        # https://chadoslkii-ecomm.s3.ap-northeast-2.amazonaws.com/media/1368047093/1368047093.JPG
        # s3://chadoslkii-ecomm/media/1368047093/1368047093.JPG
        if aws_obj_key:
            headers = None
            if download:
                filename = self.get_filename(path, new_filename=new_filename)
                headers = {
                    'response-content-type': 'application/force-download',
                    'response-content-disposition': 'attachment;filename="%s"' % filename
                }
            file_url = aws_obj_key.generate_url(
                response_headers=headers,
                expires_in=self.expires,
                method='GET')
        return file_url
