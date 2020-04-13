from abc import ABC

from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy import Column, Integer, MetaData, Sequence, String, Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper, relationship

from epical.entities.department import Department
from epical.entities.province import Province
from epical.entities.user import User

__all__ = [
    "DepartmentRepositoryInterface",
    "DepartmentRepository",
    "department_mapping",
]


class DepartmentRepositoryInterface(ABC):
    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def add(self, department: Department):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")

    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def find_all(self):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")


class DepartmentRepository(DepartmentRepositoryInterface):
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def add(self, department: Department):
        try:
            self.db.session.add(department)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

    def find_all(self):
        return self.db.session.query(Department).all()


def department_mapping(metadata: MetaData):
    department = Table(
        "departments",
        metadata,
        Column(
            "id",
            Integer,
            Sequence("departments_id_seq"),
            nullable=False,
            primary_key=True,
        ),
        Column("name", String(160), nullable=False, unique=True),
    )

    mapper(
        Department,
        department,
        properties={
            "province": relationship(
                Province, backref="department", order_by=department.c.id
            ),
            "user": relationship(User, backref="department", order_by=department.c.id),
        },
    )

    return department
