import numpy as np

from flask_restful import Resource
from http import HTTPStatus
from models.covid_sir_d import CovidSirD


class CovidSirDResource(Resource):
    @staticmethod
    def get():
        model_sird = CovidSirD()
        data, time = model_sird.model(initial_conditions=np.array([32000000., 6., 0., 0.]), duration=120)
        ds_dt = data[:, 0]
        di_dt = data[:, 1]
        dr_dt = data[:, 2]
        dd_dt = data[:, 3]
        time = np.around(time, decimals=2)

        return {'susceptible': ds_dt.tolist(),
                'infected': di_dt.tolist(),
                'recovered': dr_dt.tolist(),
                'death': dd_dt.tolist(),
                'time': time.tolist()}, HTTPStatus.OK

