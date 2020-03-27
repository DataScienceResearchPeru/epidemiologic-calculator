from flask import request
from flask_restful import Resource
from injector import inject
from http import HTTPStatus
from repositories.i_user_repository import IUserRepository
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

        return {"message": "User with given email already exists"}, HTTPStatus.BAD_REQUEST


class UserLoginResource(Resource):
    @inject
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get(self):
        pass

    def post(self):
        data = request.get_json()

        try:
            user = self.user_repository.get_user_by_email(data['email'])

            if user.valid_credential(data['password']):
                return HTTPStatus.OK
        except Exception:
            pass

        return {"message": "Invalid username or password"}, HTTPStatus.BAD_REQUEST
