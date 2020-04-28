from flask import Flask
from injector import Binder, singleton

from .mail import EmailService, EmailServiceInterface
from .aws_s3 import AmazonS3Service, AmazonS3ServiceInterface

__all__ = ["bind_services"]


def bind_services(binder: Binder) -> Binder:
    application = binder.injector.get(Flask)
    email_service = EmailService(application)
    amazon_s3 = AmazonS3Service(application)
    binder.bind(EmailServiceInterface, email_service, scope=singleton)
    binder.bind(AmazonS3ServiceInterface, amazon_s3, scope=singleton)
    return binder
