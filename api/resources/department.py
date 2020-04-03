from flask_restful import Resource
from injector import inject
from http import HTTPStatus

from repositories.i_department_repository import IDepartmentRepository


class DepartmentListResource(Resource):
    @inject
    def __init__(self, department_repository: IDepartmentRepository):
        self.department_repository = department_repository

    def get(self):
        departments = self.department_repository.find_all()
        return {'departments': list(map(lambda department: department.to_dict(), departments))}, HTTPStatus.OK
