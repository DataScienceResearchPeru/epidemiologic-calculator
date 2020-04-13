from abc import ABC

from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    MetaData,
    Sequence,
    String,
    Table,
    func,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper

from epical.entities.user import User

__all__ = [
    "UserRepositoryInterface",
    "UserRepository",
    "user_mapping",
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

        return None


def user_mapping(metadata: MetaData):
    user = Table(
        "users",
        metadata,
        Column(
            "id", Integer, Sequence("users_id_seq"), nullable=False, primary_key=True
        ),
        Column("first_name", String(120)),
        Column("last_name", String(120)),
        Column("institution", String(200)),
        Column("email", String(120), unique=True),
        Column("encrypted_password", LargeBinary(60)),
        Column("confirm_email", Boolean),
        Column("department_id", Integer, ForeignKey("departments.id")),
        Column("province_id", Integer, ForeignKey("provinces.id")),
        Column("district_id", Integer, ForeignKey("districts.id")),
        Column("created_at", DateTime(), nullable=False, server_default=func.now()),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )

    mapper(User, user)

    return user
