import boto3
import uuid
from datetime import datetime
from django.conf import settings
from rest_framework import serializers

def s3_file_upload_by_file_date(upload_file, bucket_path,
                                content_type=None, extension=None):
    print(f'@@@@@@@@@@@@ s3_file_upload_by_file_date : {upload_file}')
    # bucket_name = bucket_name.replqce('/', '')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    if content_type:
        content_type = content_type
    else:
        content_type = upload_file.content_type
    if extension:
        extension = extension
    else:
        extension = upload_file.name.split('.')[-1]

    now = datetime.now()
    random_str = str(uuid.uuid4())
    random_file_name = f'{now}_{random_str}.{extension}'
    upload_file_path_name = f'{bucket_path}/{random_file_name}'

    try:
        upload_file.seek(0)
    except Exception:
        pass

    s3 = boto3.resource('s3', region_name=settings.AWS_S3_REGION_NAME,
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    if s3.Bucket(bucket_name).put_object(Key=upload_file_path_name,
                                         Body=upload_file,
                                         ContentType=content_type) is not None:
        return f'https://s3-{settings.AWS_S3_REGION_NAME}.amazonaws.com/{bucket_name}/{bucket_path}/{random_file_name}'
    return False