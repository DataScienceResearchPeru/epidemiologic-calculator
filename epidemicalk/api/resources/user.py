from datetime import timedelta
from http import HTTPStatus

from boto3.s3.transfer import S3Transfer
from flask import render_template, request
from flask_jwt_extended import create_access_token, decode_token
from flask_restful import Resource
from injector import inject
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError

from epidemicalk.conf import Settings
from epidemicalk.entities.user import User
from epidemicalk.repositories.exceptions import InvalidUserException
from epidemicalk.repositories.user import UserRepositoryInterface
from epidemicalk.services.mail import EmailServiceInterface
from mimetypes import guess_extension, guess_type

import uuid

class UserListResource(Resource):
    @inject
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        email_service: EmailServiceInterface,
    ):
        self.user_repository = user_repository
        self.email_service = email_service

    def get(self):  # pylint: disable=no-self-use
        return {}, HTTPStatus.BAD_REQUEST

    def post(self):
        data = request.get_json()

        try:
            self.user_repository.get_user_by_email(data["email"])
        except InvalidUserException:
            user = User(
                first_name=data["firstName"],
                last_name=data["lastName"],
                institution=data["institution"],
                email=data["email"],
                password=data["password"],
                department_id=data["departmentId"],
                province_id=data["provinceId"],
                district_id=data["districtId"],
                confirm_email=False,
            )

            self.user_repository.add(user)

            expires = timedelta(hours=24)
            token = create_access_token(str(user.email), expires_delta=expires)
            url = Settings.HOST_URL + "verify_account/" + token

            body_html = render_template(
                "messages/confirm_email.html",
                full_name=user.full_name(),
                confirm_url=url,
            )
            body_text = render_template(
                "messages/confirm_email.txt",
                full_name=user.full_name(),
                confirm_url=url,
            )
            data_message = {
                "to": user.email,
                "subject": "Por favor, verifique su dirección de correo electrónico",
                "sender": ("Data Science Research Perú", "support@datascience.com"),
                "content_html": body_html,
                "content_text": body_text,
            }

            if self.email_service.send(data_message):
                return user.to_dict(), HTTPStatus.OK

            return (
                {"message": "Error al enviar el mensaje"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        return {"message": "El correo electrónico ya fue usado"}, HTTPStatus.BAD_REQUEST


class UserSendEmailResource(Resource):
    @inject
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        email_service: EmailServiceInterface,
    ):
        self.user_repository = user_repository
        self.email_service = email_service

    def post(self):
        data = request.get_json()

        try:
            user = self.user_repository.get_user_by_email(data["email"])
            expires = timedelta(hours=24)
            token = create_access_token(str(user.email), expires_delta=expires)
            url = Settings.HOST_URL + "verify_account/" + token

            body_html = render_template(
                "messages/confirm_email.html",
                full_name=user.full_name(),
                confirm_url=url,
            )
            body_text = render_template(
                "messages/confirm_email.txt",
                full_name=user.full_name(),
                confirm_url=url,
            )

            data_message = {
                "to": user.email,
                "subject": "Por favor, verifique su dirección de correo electrónico",
                "sender": ("Data Science Research Perú", "support@datascience.com"),
                "content_html": body_html,
                "content_text": body_text,
            }

            if self.email_service.send(data_message):
                return user.to_dict(), HTTPStatus.OK

            return (
                {"message": "Error al enviar el mensaje"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        except InvalidUserException:
            print("Invalid user")

        return (
            {"message": "El correo electrónico no se encuentra registrado"},
            HTTPStatus.BAD_REQUEST,
        )


class UserVerifyAccountResource(Resource):
    @inject
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def get(self):
        pass

    def post(self):
        data = request.get_json()
        token = data.get("token")

        try:
            email = decode_token(token)["identity"]
            user = self.user_repository.get_user_by_email(email)
            user.active_email()
            self.user_repository.add(user)

            return (
                {"message": "El correo electrónico fue confirmado con éxito"},
                HTTPStatus.OK,
            )

        except ExpiredSignatureError as e:
            print("error: {0}".format(e))
        except (DecodeError, InvalidTokenError) as e:
            print("error: {0}".format(e))
        except InvalidUserException:
            print("Invalid user")

        return (
            {"message": "El enlace no es válido o ha expirado"},
            HTTPStatus.BAD_REQUEST,
        )


class UserLoginResource(Resource):
    @inject
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def get(self):  # pylint: disable=no-self-use
        return {}, HTTPStatus.BAD_REQUEST

    def post(self):
        data = request.get_json()
        email = data.get("username")
        password = data.get("password")

        try:
            user = self.user_repository.get_user_by_email(email=email)

            if user.is_active_email():
                if user.valid_credential(  # pylint: disable=no-else-return
                    password=password
                ):
                    access_token = create_access_token(identity=email)
                    return (
                        {"full_name": user.full_name(), "access_token": access_token},
                        HTTPStatus.OK,
                    )
                else:
                    return (
                        {"message": "La contraseña es incorrecta"},
                        HTTPStatus.UNAUTHORIZED,
                    )
            return (
                {"message": "El correo electrónico no se ha verificado"},
                HTTPStatus.BAD_REQUEST,
            )
        except InvalidUserException:
            return (
                {"message": "El usuario no se encuentra registrado"},
                HTTPStatus.UNAUTHORIZED,
            )


class UserForgotPasswordResource(Resource):
    @inject
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        email_service: EmailServiceInterface,
    ):
        self.user_repository = user_repository
        self.email_service = email_service

    def post(self):
        data = request.get_json()
        email = data.get("email")
        url = Settings.HOST_URL + "reset-password/"

        try:
            user = self.user_repository.get_user_by_email(email=email)

            expires = timedelta(hours=24)
            reset_token = create_access_token(str(user.email), expires_delta=expires)
            body_html = render_template(
                "messages/password_reset_email.html",
                full_name=user.full_name(),
                password_reset_url=url + reset_token,
            )
            body_text = render_template(
                "messages/password_reset_email.txt",
                full_name=user.full_name(),
                password_reset_url=url + reset_token,
            )

            data_message = {
                "to": user.email,
                "subject": "Restablece tu contraseña",
                "sender": ("Data Science Research Perú", "support@datascience.com"),
                "content_html": body_html,
                "content_text": body_text,
            }

            if self.email_service.send(data_message):
                return (
                    {
                        "message": "Por favor revise su correo electrónico para el"
                        " enlace de restablecimiento de contraseña"
                    },
                    HTTPStatus.OK,
                )
            return (
                {"message": "Error al enviar el mensaje"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        except InvalidUserException:
            print("Invalid user")

        return (
            {"message": "El correo electrónico no está registrado"},
            HTTPStatus.BAD_REQUEST,
        )


class UserResetPasswordResource(Resource):
    @inject
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        email_service: EmailServiceInterface,
    ):
        self.user_repository = user_repository
        self.email_service = email_service

    def post(self):
        data = request.get_json()
        new_password = data.get("newPassword")
        reset_token = data.get("resetToken")

        try:
            email = decode_token(reset_token)["identity"]
            user = self.user_repository.get_user_by_email(email)
            user.change_password(new_password)
            self.user_repository.add(user)

            return {"message": "La contraseña fue cambiada exitosamente"}, HTTPStatus.OK

        except ExpiredSignatureError as e:
            print("error: {0}".format(e))
        except (DecodeError, InvalidTokenError) as e:
            print("error: {0}".format(e))
        except InvalidUserException:  # pylint: disable=broad-except
            print("Invalid user")

        return (
            {
                "message": "El enlace para restablecer la contraseña no es válido "
                "o ha expirado"
            },
            HTTPStatus.BAD_REQUEST,
        )


class UserResource(Resource):
    @inject
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def upload_file(self, image_base64):
        import boto3
        import base64
        import os
        access_key = Settings.AWS_ACCESS_KEY
        secret_key = Settings.AWS_ACCESS_SECRET
        session = boto3.session.Session()
        name_file = uuid.uuid4()
        extension = guess_extension(guess_type(image_base64)[0])
        name_file = str(name_file) + extension
        image_base64 = image_base64.replace("data:image/png;base64,", "")
        image_base64 = image_base64.replace("data:image/jpeg;base64,", "")
        img_data = image_base64.encode()
        with open(name_file, "wb") as fh:
            fh.write(base64.decodebytes(img_data))
        client = session.client('s3', region_name=Settings.AWS_REGION, aws_access_key_id=access_key,aws_secret_access_key=secret_key)
        # response_file = client.upload_file(name_file, Settings.AWS_S3_BUCKET, name_file)
        transfer = S3Transfer(client)
        transfer.upload_file(name_file, Settings.AWS_S3_BUCKET, name_file, extra_args={'ACL': 'private'})
        file_url = '%s/%s/%s' % (client.meta.endpoint_url, Settings.AWS_S3_BUCKET, name_file)
        os.remove(name_file)
        return file_url

    def post(self):
        data = request.get_json()
        email = data.get("email")
        image_base64 = data.get("image")
        url_s3 = self.upload_file(image_base64)
        image_profile = url_s3

        try:
            user = self.user_repository.get_user_by_email(email)
            new_user = user.to_update(img_profile=image_profile)
            self.user_repository.update(uid=user.id, user=new_user)

            return {"message": "El usuario se actualizó exitosamente"}, HTTPStatus.OK

        except InvalidUserException:
            return {"message": "El usuario es inválido"}, HTTPStatus.BAD_REQUEST
