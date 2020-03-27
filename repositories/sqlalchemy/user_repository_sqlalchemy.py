from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.exc import IntegrityError

from entities.user import User
from repositories.i_user_repository import IUserRepository


class UserRepositorySqlAlchemy(IUserRepository):

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
        raise
