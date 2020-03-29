from flask import request, render_template, url_for
from flask_restful import Resource
from injector import inject
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from repositories.i_user_repository import IUserRepository
from services.i_email_method_service import IEmailMethodService
from environment_config import EnvironmentConfig
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
            user = User(first_name=data['first_name'],
                        last_name=data['last_name'],
                        institution=data['institution'],
                        email=data['email'],
                        password=data['password'])

            self.user_repository.add(user)
            return user.data(), HTTPStatus.CREATED

        return {"message": "Email already used"}, HTTPStatus.BAD_REQUEST


class UserLoginResource(Resource):
    @inject
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get(self):
        pass

    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        try:
            user = self.user_repository.get_user_by_email(email=email)

            if user.valid_credential(password=password):
                access_token = create_access_token(identity=email)
                return {'access_token': access_token}, HTTPStatus.OK
        except Exception:
            pass

        return {"message": "Email or password is incorrect"}, HTTPStatus.UNAUTHORIZED


class UserResetPasswordResource(Resource):
    @inject
    def __init__(self, user_repository: IUserRepository, email_method_service: IEmailMethodService):
        self.user_repository = user_repository
        self.email_method_service = email_method_service

    def get(self):
        pass

    def post(self):
        data = request.get_json()
        email = data.get('email')

        try:
            user = self.user_repository.get_user_by_email(email=email)

            password_reset_serializer = URLSafeTimedSerializer(EnvironmentConfig.SECRET_KEY)
            token = password_reset_serializer.dumps(email, salt='password-reset-salt')

            template = render_template("messages/password_reset_email.html",
                                       password_reset_url=url_for('.edit-password', token=token,
                                                                  _external=True))
            data_message = {
                'to': user.email,
                'subject': 'Restablece tu contraseña',
                'content': template
            }

            if self.email_method_service.send_message(data_message):
                return {"message": "Please check your email for the reset password link"}, HTTPStatus.OK
            else:
                return {"message": "Error sending the message"}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            print("error: {0}".format(e))

        return {"message": "Email is not registered"}, HTTPStatus.NOT_FOUND


class UserEditPasswordResource(Resource):
    @inject
    def __init__(self, user_repository: IUserRepository, email_method_service: IEmailMethodService):
        self.user_repository = user_repository
        self.email_method_service = email_method_service

    def get(self, token):
        password_reset_serializer = URLSafeTimedSerializer(EnvironmentConfig.SECRET_KEY)

        try:
            email = password_reset_serializer.loads(token,
                                                    salt='password-reset-salt',
                                                    max_age=600)
            return {"message": "Valid token "}, HTTPStatus.OK

        except SignatureExpired as e:
            print("error: {0}".format(e))
        except BadTimeSignature as e:
            print("error: {0}".format(e))

        return {"message": "The link to reset the password is invalid or has expired"}, HTTPStatus.BAD_REQUEST

    def post(self, token):
        password_reset_serializer = URLSafeTimedSerializer(EnvironmentConfig.SECRET_KEY)
        data = request.get_json()
        password = data.get('password')
        new_password = data.get('new_password')

        if password != new_password:
            return {"message": "Passwords do not match"}, HTTPStatus.BAD_REQUEST

        try:
            email = password_reset_serializer.loads(token,
                                                    salt='password-reset-salt',
                                                    max_age=600)
            user = self.user_repository.get_user_by_email(email)
            user.change_password(new_password)
            self.user_repository.add(user)

        except SignatureExpired as e:
            print("error: {0}".format(e))
        except BadTimeSignature as e:
            print("error: {0}".format(e))

        except Exception as e:
            print("error: {0}".format(e))

        return {"message": "The link to reset the password is invalid or has expired"}, HTTPStatus.BAD_REQUEST
