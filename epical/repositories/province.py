from abc import ABC

from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy import Column, ForeignKey, Integer, MetaData, Sequence, String, Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper, relationship

from epical.entities.district import District
from epical.entities.province import Province
from epical.entities.user import User

__all__ = [
    "ProvinceRepositoryInterface",
    "ProvinceRepository",
    "province_mapping",
]


class ProvinceRepositoryInterface(ABC):
    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def add(self, province: Province):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")

    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def find_all(self):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")

    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def find_by_department(self, department_id: int):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")


class ProvinceRepository(ProvinceRepositoryInterface):
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def add(self, province: Province):
        try:
            self.db.session.add(province)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            # raise IntegrityError(msg)

    def find_all(self):
        return self.db.session.query(Province).all()

    def find_by_department(self, department_id: int):
        provinces = (
            self.db.session.query(Province)
            .filter(Province.department_id == department_id)
            .all()
        )

        if provinces:
            return provinces

        return None


def province_mapping(metadata: MetaData):
    province = Table(
        "provinces",
        metadata,
        Column(
            "id",
            Integer,
            Sequence("provinces_id_seq"),
            nullable=False,
            primary_key=True,
        ),
        Column("name", String(160), nullable=False, unique=True),
        Column("department_id", Integer, ForeignKey("departments.id")),
    )

    mapper(
        Province,
        province,
        properties={
            "district": relationship(
                District, backref="province", order_by=province.c.id
            ),
            "user": relationship(User, backref="province", order_by=province.c.id),
        },
    )

    return province
