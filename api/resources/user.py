from flask import request, render_template
from flask_restful import Resource
from injector import inject
from flask_jwt_extended import create_access_token, decode_token
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from datetime import timedelta
from http import HTTPStatus
from repositories.i_user_repository import IUserRepository
from services.i_email_method_service import IEmailMethodService
from entities.user import User


class UserListResource(Resource):
    @inject
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get(self):
        pass

    def post(self):
        data = request.get_json()

        try:
            self.user_repository.get_user_by_email(data['email'])
        except Exception:
            user = User(first_name=data['firstName'],
                        last_name=data['lastName'],
                        institution=data['institution'],
                        email=data['email'],
                        password=data['password'])

            self.user_repository.add(user)
            return user.to_dict(), HTTPStatus.CREATED

        return {"message": "Email already used"}, HTTPStatus.BAD_REQUEST


class UserLoginResource(Resource):
    @inject
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get(self):
        pass

    def post(self):
        data = request.get_json()
        email = data.get('username')
        password = data.get('password')

        try:
            user = self.user_repository.get_user_by_email(email=email)

            if user.valid_credential(password=password):
                access_token = create_access_token(identity=email)
                return {'full_name': user.full_name(), 'access_token': access_token}, HTTPStatus.OK
        except Exception:
            pass

        return {"message": "Email or password is incorrect"}, HTTPStatus.UNAUTHORIZED


class UserForgotPasswordResource(Resource):
    @inject
    def __init__(self, user_repository: IUserRepository, email_method_service: IEmailMethodService):
        self.user_repository = user_repository
        self.email_method_service = email_method_service

    def post(self):
        data = request.get_json()
        email = data.get('email')
        url = request.host_url + 'reset-password/'

        try:
            user = self.user_repository.get_user_by_email(email=email)

            expires = timedelta(hours=24)
            reset_token = create_access_token(str(user.email), expires_delta=expires)
            body_html = render_template("messages/password_reset_email.html", password_reset_url=url + reset_token)
            body_text = render_template("messages/password_reset_email.txt", password_reset_url=url + reset_token)

            data_message = {
                'to': user.email,
                'subject': 'Restablece tu contraseña',
                'sender': ("Data Science Research Perú", "support@datascience.com"),
                'content_html': body_html,
                'content_text': body_text
            }

            if self.email_method_service.send_message(data_message):
                return {"message": "Please check your email for the reset password link"}, HTTPStatus.OK
            else:
                return {"message": "Error sending the message"}, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            print("error: {0}".format(e))

        return {"message": "Email is not registered"}, HTTPStatus.BAD_REQUEST


class UserResetPasswordResource(Resource):
    @inject
    def __init__(self, user_repository: IUserRepository, email_method_service: IEmailMethodService):
        self.user_repository = user_repository
        self.email_method_service = email_method_service

    def post(self):
        data = request.get_json()
        new_password = data.get('newPassword')
        reset_token = data.get('resetToken')

        try:
            email = decode_token(reset_token)['identity']
            user = self.user_repository.get_user_by_email(email)
            user.change_password(new_password)
            self.user_repository.add(user)

            return {"message": "Password was successfully changed"}, HTTPStatus.OK

        except ExpiredSignatureError as e:
            print("error: {0}".format(e))
        except (DecodeError, InvalidTokenError) as e:
            print("error: {0}".format(e))
        except Exception as e:
            print("error Exception: {0}".format(e))

        return {"message": "The link to reset the password is invalid or has expired"}, HTTPStatus.BAD_REQUEST
