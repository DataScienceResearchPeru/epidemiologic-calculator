from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.exc import IntegrityError

from entities.department import Departament
from repositories.i_departament_repository import IDepartamentRepository


class DepartamentRepositorySqlAlchemy(IDepartamentRepository):

    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def add(self, departament: Departament):
        try:
            self.db.session.add(departament)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

    def find_all(self):
        return self.db.session.query(Departament).all()

