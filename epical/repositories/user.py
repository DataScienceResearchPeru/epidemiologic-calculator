from abc import ABC

from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.exc import IntegrityError

from epical.entities.user import User

from .exceptions import InvalidUserException

__all__ = [
    "UserRepositoryInterface",
    "UserRepository",
]


class UserRepositoryInterface(ABC):
    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def add(self, user: User):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")

    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def get_user_by_email(self, email: str):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")


class UserRepository(UserRepositoryInterface):
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def add(self, user: User):
        try:
            self.db.session.add(user)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

    def get_user_by_email(self, email: str):
        user = self.db.session.query(User).filter(User.email == email).first()
        if user:
            return user
        raise InvalidUserException
