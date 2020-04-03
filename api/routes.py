from flask import Blueprint
from flask_restful import Api
from api.resources.covid_epidemiology import CovidSirDResource, CovidSeirDResource, CovidSeaichurDResource
from api.resources.user import UserListResource, UserLoginResource, UserForgotPasswordResource, \
                                UserResetPasswordResource
from api.resources.department import DepartmentListResource
from api.resources.province import ProvinceListResource
from api.resources.district import DistrictListResource


api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp)


api_rest.add_resource(CovidSirDResource, '/sird')
api_rest.add_resource(CovidSeirDResource, '/seird')
api_rest.add_resource(CovidSeaichurDResource, '/seaichurd')
api_rest.add_resource(UserListResource, '/users')
api_rest.add_resource(UserLoginResource, '/user/login')
api_rest.add_resource(UserForgotPasswordResource, '/user/forgot-password')
api_rest.add_resource(UserResetPasswordResource, '/user/reset-password')
api_rest.add_resource(DepartmentListResource, '/departments')
api_rest.add_resource(ProvinceListResource, *['/provinces', '/departments/<int:department_id>/provinces'])
api_rest.add_resource(DistrictListResource, *['/districts', '/provinces/<int:province_id>/districts'])
