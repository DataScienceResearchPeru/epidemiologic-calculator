from abc import ABC

from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy import Column, ForeignKey, Integer, MetaData, Sequence, String, Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapper, relationship

from epical.entities.district import District
from epical.entities.user import User

__all__ = [
    "DistrictRepositoryInterface",
    "DistrictRepository",
    "district_mapping",
]


class DistrictRepositoryInterface(ABC):
    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def add(self, district: District):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")

    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def find_all(self):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")

    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def find_by_province(self, province_id: int):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")


class DistrictRepository(DistrictRepositoryInterface):
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def add(self, district: District):
        try:
            self.db.session.add(district)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

    def find_all(self):
        return self.db.session.query(District).all()

    def find_by_province(self, province_id: int):
        districts = (
            self.db.session.query(District)
            .filter(District.province_id == province_id)
            .all()
        )

        if districts:
            return districts

        return None


def district_mapping(metadata: MetaData):
    district = Table(
        "districts",
        metadata,
        Column(
            "id",
            Integer,
            Sequence("districts_id_seq"),
            nullable=False,
            primary_key=True,
        ),
        Column("name", String(160), nullable=False),
        Column("province_id", Integer, ForeignKey("provinces.id")),
    )

    mapper(
        District,
        district,
        properties={
            "user": relationship(User, backref="district", order_by=district.c.id)
        },
    )

    return district
