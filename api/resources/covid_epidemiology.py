import numpy as np

from flask_restful import Resource
from http import HTTPStatus
from models.covid_sir_d import CovidSirD


class CovidSirDResource(Resource):
    @staticmethod
    def get():
        model_sird = CovidSirD()
        data, time = model_sird.model(initial_conditions=np.array([32000000., 6., 0., 0.]), duration=120)

        return {'data': data, 'time': time}, HTTPStatus.OK
