from injector import Binder, singleton

from services.i_email_method_service import IEmailMethodService
from services.mail_email_method_service import MailEmailMethodService


def configure_services_binding(binder: Binder) -> Binder:
    binder.bind(IEmailMethodService, MailEmailMethodService, scope=singleton)
    return binder
