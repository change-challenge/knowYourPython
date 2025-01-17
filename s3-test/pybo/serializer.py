import logging
import uuid

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from rest_framework import serializers

logger = logging.getLogger(__name__)

class PresignedURLSerializer(serializers.Serializer):
    url = serializers.ListSerializer(
        read_only=True,
        child=serializers.URLField(read_only=True)
    )
    image_list = serializers.ListSerializer(
        write_only=True,
        child=serializers.CharField(write_only=True)
    )

    def validate(self, attrs):
        print("@@@@@@@@@@ validate 시작")
        print("attrs:", attrs)
        url_list = []

        for image in attrs.get('image_list', []):
            url = self.create_presigned_url(image=image)
            url_list.append(url)

        attrs['url'] = url_list
        return attrs

    @staticmethod
    def create_presigned_url(
            image,
            content_type='images',
            aws_access_key_id=None,
            aws_secret_access_key=None,
            expiration=3600):

        config = Config(signature_version="s3v4")

        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='ap-northeast-2',
            config=config
        )
        try:
            print(f"Creating presigned URL for image: {image}")

            name = image.split('.')
            object_ket = '/'.join([f'media/{content_type}', f'{str(uuid.uuid4())}.{name[-1]}'])

            url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': 'test-hojin-bucket',
                    'Key': object_ket,
                },
                ExpiresIn=expiration,
            )
            logger.info(f'Got presigned URL: {url}')
        except ClientError as e:
            logger.error(e)
            return None
        return url

    def create(self, validated_data):
        logger.info('s3 presigend url')
        logger.info(validated_data)
        return validated_data
