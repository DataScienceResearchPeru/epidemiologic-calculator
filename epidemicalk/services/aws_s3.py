import os
from abc import ABC

import boto3
from s3transfer import S3Transfer

from epidemicalk.conf import Settings
from epidemicalk.services.image import clean_base64, generate_name_random, save_image

__all__ = [
    "AmazonS3ServiceInterface",
    "AmazonS3Service",
]


class AmazonS3ServiceInterface(ABC):
    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def upload(self, image_base64: str):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")


class AmazonS3Service(AmazonS3ServiceInterface):
    def __init__(self, app):
        self.app = app
        access_key = Settings.AWS_ACCESS_KEY
        secret_key = Settings.AWS_ACCESS_SECRET
        session = boto3.session.Session()
        self.client = session.client(
            "s3",
            region_name=Settings.AWS_REGION,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def upload(self, image_base64: str):
        name_file = generate_name_random(image_base64)
        image_base64 = clean_base64(image_base64)
        save_image(image_base64, name_file)
        transfer = S3Transfer(self.client)
        transfer.upload_file(
            name_file, Settings.AWS_S3_BUCKET, name_file, extra_args={"ACL": "private"}
        )
        file_url = "%s/%s/%s" % (
            self.client.meta.endpoint_url,
            Settings.AWS_S3_BUCKET,
            name_file,
        )
        os.remove(name_file)
        return file_url
