from http import HTTPStatus

from flask_restful import Resource
from injector import inject

from epidemicalk.repositories.department import DepartmentRepositoryInterface


class DepartmentListResource(Resource):
    @inject
    def __init__(self, department_repository: DepartmentRepositoryInterface):
        self.department_repository = department_repository

    def get(self):
        departments = self.department_repository.find_all()
        return (
            {"departments": [department.to_dict() for department in departments]},
            HTTPStatus.OK,
        )
