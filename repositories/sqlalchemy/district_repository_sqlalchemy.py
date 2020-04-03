from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.exc import IntegrityError

from entities.district import District
from repositories.i_district_repository import IDistrictRepository


class DistrictRepositorySqlAlchemy(IDistrictRepository):

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
        districts = self.db.session.query(District).filter(District.province_id == province_id).all()

        if districts:
            return districts
        raise
