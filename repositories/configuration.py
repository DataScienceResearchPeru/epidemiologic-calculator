from injector import Binder

from repositories.i_user_repository import IUserRepository
from repositories.sqlalchemy.user_repository_sqlalchemy import UserRepositorySqlAlchemy


def configure_repositories_binding(binder: Binder)-> Binder:
    binder.bind(IUserRepository, UserRepositorySqlAlchemy)