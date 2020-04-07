from flask import Blueprint
from flask_restful import Api
from api.resources.covid_epidemiology import CovidSirDResource, CovidSeirDResource, CovidSeaichurDResource
from api.resources.user import UserListResource, UserLoginResource, UserForgotPasswordResource, UserResetPasswordResource


api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp)


api_rest.add_resource(CovidSirDResource, '/sird','/sird/<float:a1p>')
api_rest.add_resource(CovidSeirDResource, '/seird')
api_rest.add_resource(CovidSeaichurDResource, '/seaichurd')
api_rest.add_resource(UserListResource, '/users')
api_rest.add_resource(UserLoginResource, '/user/login')
api_rest.add_resource(UserForgotPasswordResource, '/user/forgot-password')
api_rest.add_resource(UserResetPasswordResource, '/user/reset-password')
