from http import HTTPStatus

from flask_restful import Resource
from injector import inject

from epical.repositories.district import DistrictRepositoryInterface


class DistrictListResource(Resource):
    @inject
    def __init__(self, district_repository: DistrictRepositoryInterface):
        self.district_repository = district_repository

    def get(self, province_id=None):
        if province_id:
            districts = self.district_repository.find_by_province(
                province_id=province_id
            )
        else:
            districts = self.district_repository.find_all()

        return (
            {"districts": [district.to_dict() for district in districts]},
            HTTPStatus.OK,
        )
