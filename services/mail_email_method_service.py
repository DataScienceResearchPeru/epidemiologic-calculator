from flask_mail import Message, Mail
from threading import Thread
from services.i_email_method_service import IEmailMethodService
from smtplib import SMTPException, SMTPAuthenticationError
from configuration_database import app


def send_async_email(mail: Mail, message: Message):
    with app.app_context():
        try:
            mail.send(message)
        except ConnectionRefusedError:
            print("[MAIL SERVER] not working")
            raise


class MailEmailMethodService(IEmailMethodService):

    def __init__(self):
        self.mail = Mail()
        self.mail.init_app(app)

    def send_message(self, data_message: dict):
        message = Message(
            subject=data_message['subject'],
            sender=data_message['sender'],
            recipients=[data_message['to']],
            body=data_message['content_text'],
            html=data_message['content_html']
        )

        try:
            Thread(target=send_async_email, args=(self.mail, message)).start()
            return True
        except SMTPAuthenticationError as e:
            print("error: {0}".format(e))

        except SMTPException as e:
            print("error: {0}".format(e))

        return False

