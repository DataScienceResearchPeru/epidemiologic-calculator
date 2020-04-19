from abc import ABC
from smtplib import SMTPAuthenticationError, SMTPException
from threading import Thread

from flask_mail import Mail, Message

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
    def __init__(self, app):
        self.mail = Mail()
        self.app = app
        self.mail.init_app(self.app)

    def _send_email(self, mail: Mail, message: Message):
        with self.app.app_context():
            try:
                mail.send(message)
            except ConnectionRefusedError as msg:
                self.app.logger.warning("%(msg)s" % {"msg": msg})

    def send(self, message_data: dict):
        message = Message(
            subject=message_data["subject"],
            sender=message_data["sender"],
            recipients=[message_data["to"]],
            body=message_data["content_text"],
            html=message_data["content_html"],
        )

        try:
            Thread(target=self._send_email, args=(self.mail, message)).start()
            return True

        except SMTPAuthenticationError as msg:
            self.app.logger.warning("%(msg)s" % {"msg": msg})

        except SMTPException as msg:
            self.app.logger.warning("%(msg)s" % {"msg": msg})

        return False
