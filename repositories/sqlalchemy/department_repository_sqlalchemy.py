from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.exc import IntegrityError

from entities.department import Department
from repositories.i_department_repository import IDepartmentRepository


class DepartmentRepositorySqlAlchemy(IDepartmentRepository):

    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def add(self, departament: Department):
        try:
            self.db.session.add(departament)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise

    def find_all(self):
        return self.db.session.query(Department).all()

