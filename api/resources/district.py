from flask import request
from flask_restful import Resource
from injector import inject
from http import HTTPStatus

from repositories.i_district_repository import IDistrictRepository


class DistrictListResource(Resource):
    @inject
    def __init__(self, district_repository: IDistrictRepository):
        self.district_repository = district_repository

    def get(self, province_id=None):
        if province_id:
            districts = self.district_repository.find_by_province(province_id=province_id)
        else:
            districts = self.district_repository.find_all()

        return {'districts': list(map(lambda district: district.to_dict(), districts))}, HTTPStatus.OK
