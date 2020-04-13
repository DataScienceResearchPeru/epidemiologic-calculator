from injector import Binder, singleton

from .mail import EmailService, EmailServiceInterface

__all__ = ["bind_services"]


def bind_services(binder: Binder) -> Binder:
    binder.bind(EmailServiceInterface, EmailService, scope=singleton)
    return binder
