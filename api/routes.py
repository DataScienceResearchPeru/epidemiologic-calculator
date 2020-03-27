from flask import Blueprint
from flask_restful import Api
from api.resources.covid_epidemiology import CovidSirDResource, CovidSeirDResource, CovidSeaichurDResource
from api.resources.user import UserListResource

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp)


api_rest.add_resource(CovidSirDResource, '/sird')
api_rest.add_resource(CovidSeirDResource, '/seird')
api_rest.add_resource(CovidSeaichurDResource, '/seaichurd')
api_rest.add_resource(UserListResource, '/users')
