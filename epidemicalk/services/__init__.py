from flask import Flask
from injector import Binder, singleton

from .mail import EmailService, EmailServiceInterface

__all__ = ["bind_services"]


def bind_services(binder: Binder) -> Binder:
    application = binder.injector.get(Flask)
    email_service = EmailService(application)
    binder.bind(EmailServiceInterface, email_service, scope=singleton)
    return binder
