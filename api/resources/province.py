from flask import request
from flask_restful import Resource
from injector import inject
from http import HTTPStatus

from repositories.i_province_repository import IProvinceRepository


class ProvinceListResource(Resource):
    @inject
    def __init__(self, province_repository: IProvinceRepository):
        self.province_repository = province_repository

    def get(self, department_id=None):

        if department_id:
            provinces = self.province_repository.find_by_department(department_id=department_id)
        else:
            provinces = self.province_repository.find_all()

        return {'provinces': list(map(lambda province: province.to_dict(), provinces))}, HTTPStatus.OK
