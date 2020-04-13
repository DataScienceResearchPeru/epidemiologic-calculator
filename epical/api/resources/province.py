from http import HTTPStatus

from flask_restful import Resource
from injector import inject

from epical.repositories.province import ProvinceRepositoryInterface


class ProvinceListResource(Resource):
    @inject
    def __init__(self, province_repository: ProvinceRepositoryInterface):
        self.province_repository = province_repository

    def get(self, department_id=None):

        if department_id:
            provinces = self.province_repository.find_by_department(
                department_id=department_id
            )
        else:
            provinces = self.province_repository.find_all()

        return (
            {"provinces": [province.to_dict() for province in provinces]},
            HTTPStatus.OK,
        )
