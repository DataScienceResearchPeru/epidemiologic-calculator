from flask import Blueprint
from flask_restful import Api
from api.resources.covid_epidemiology import CovidSirDResource

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp)


api_rest.add_resource(CovidSirDResource, '/sird')
