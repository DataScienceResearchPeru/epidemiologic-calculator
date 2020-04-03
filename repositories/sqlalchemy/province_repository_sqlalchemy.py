from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.exc import IntegrityError

from entities.province import Province
from repositories.i_province_repository import IProvinceRepository


class ProvinceRepositorySqlAlchemy(IProvinceRepository):

    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def add(self, province: Province):
        try:
            self.db.session.add(province)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

    def find_all(self):
        return self.db.session.query(Province).all()

    def find_by_department(self, department_id: int):
        provinces = self.db.session.query(Province).filter(Province.department_id == department_id).all()

        if provinces:
            return provinces
        raise
