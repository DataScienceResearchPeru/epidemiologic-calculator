from abc import ABC
from smtplib import SMTPAuthenticationError, SMTPException
from threading import Thread

from flask_mail import Mail, Message

from epical.app import app as APP

__all__ = [
    "EmailServiceInterface",
    "EmailService",
]


class EmailServiceInterface(ABC):
    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def send(self, message_data: dict):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")


class EmailService(EmailServiceInterface):
    def __init__(self):
        self.mail = Mail()
        self.mail.init_app(APP)

    def _send_email(self, message: Message):
        with APP.app_context():
            try:
                self.mail.send(message)
            except ConnectionRefusedError as msg:
                APP.logger.warning("%(msg)s" % {"msg": msg})

    def send(self, message_data: dict):
        message = Message(
            subject=message_data["subject"],
            sender=message_data["sender"],
            recipients=[message_data["to"]],
            body=message_data["content_text"],
            html=message_data["content_html"],
        )

        try:
            Thread(target=self._send_email, args=(message)).start()
            return True

        except SMTPAuthenticationError as msg:
            APP.logger.warning("%(msg)s" % {"msg": msg})

        except SMTPException as msg:
            APP.logger.warning("%(msg)s" % {"msg": msg})

        return False
