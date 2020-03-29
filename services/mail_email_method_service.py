from flask_mail import Message, Mail
from flask import current_app
from services.i_email_method_service import IEmailMethodService
from smtplib import SMTPException, SMTPAuthenticationError


class MailEmailMethodService(IEmailMethodService):

    def __init__(self):
        self.mail = Mail()
        self.mail.init_app(current_app)

    def send_message(self, data_message: dict):
        message = Message(
            subject=data_message['subject'],
            sender=("Data Science Research Perú", "datascience@gmail.com"),
            recipients=[data_message['to']],
            body=data_message['content'],
            html=data_message['content']
        )

        try:
            self.mail.send(message)
            return True
        except SMTPAuthenticationError as e:
            print("error: {0}".format(e))

        except SMTPException as e:
            print("error: {0}".format(e))

        return False
