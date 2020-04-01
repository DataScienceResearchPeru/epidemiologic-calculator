import numpy as np

from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.covid_sir_d import CovidSirD
from models.covid_seir_d import CovidSeirD
from models.covid_seaichur_d import CovidSeaichurD


class CovidSirDResource(Resource):
    def get(self):
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


class CovidSeirDResource(Resource):
    @staticmethod
    def get():
        model_seird = CovidSeirD()
        data, time = model_seird.model(initial_conditions=np.array([32000000., 0., 6., 0., 0.]), duration=100)
        ds_dt = data[:, 0]
        de_dt = data[:, 1]
        di_dt = data[:, 2]
        dr_dt = data[:, 3]
        dd_dt = data[:, 4]
        time = np.around(time, decimals=2)

        return {'susceptible': ds_dt.tolist(),
                'exposed': de_dt.tolist(),
                'infected': di_dt.tolist(),
                'recovered': dr_dt.tolist(),
                'death': dd_dt.tolist(),
                'time': time.tolist()}, HTTPStatus.OK


class CovidSeaichurDResource(Resource):
    @staticmethod
    def get():
        model_seaichurd = CovidSeaichurD()
        data, time = model_seaichurd.model(initial_conditions=np.array([32000000., 0., 0., 6., 0., 0., 0., 0., 0.]),
                                           duration=120)
        ds_dt = data[:, 0]
        de_dt = data[:, 1]
        da_dt = data[:, 2]
        di_dt = data[:, 3]
        dc_dt = data[:, 4]
        dh_dt = data[:, 5]
        du_dt = data[:, 6]
        dr_dt = data[:, 7]
        dd_dt = data[:, 8]
        time = np.around(time, decimals=2)

        return {'susceptible': ds_dt.tolist(),
                'exposed': de_dt.tolist(),
                'asymptomatic': da_dt.tolist(),
                'infected': di_dt.tolist(),
                'quarantine': dc_dt.tolist(),
                'hospitalized': dh_dt.tolist(),
                'uci': du_dt.tolist(),
                'recovered': dr_dt.tolist(),
                'death': dd_dt.tolist(),
                'time': time.tolist()}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        epidemiological_parameters = {
            'A1': data.get('a1', 0.50),
            'A2': data.get('a2', 0.28),
            'A3': data.get('a3', 0.35),
            'A4': data.get('a4', 0.40),
            'A5': data.get('a5', 0.20),
            'A6': data.get('a6', 0.35),
            'A7': data.get('a7', 0.50),
            'A8': data.get('a8', 0.15),
            'A9': data.get('a9', 0.30),
            'QQ': data.get('qq', 0.0),
            'R1': data.get('r1', 0.20),
            'R2': data.get('r2', 0.15),
            'R3': data.get('r3', 0.07),
            'R4': data.get('r4', 0.03),
            'D1': data.get('d1', 0.001),
            'D2': data.get('d2', 0.002),
            'D3': data.get('d3', 0.005)
        }

        duration = data.get('duration', 120)
        population = data.get('population', 32000006)
        initial_infected = data.get('initial_infected', 6.)

        initial_exposed = 0.
        initial_asymptomatic = 0.
        initial_quarantine = 0.
        initial_hospitalized = 0.
        initial_uci = 0.
        initial_recovered = 0.
        initial_death = 0.

        initial_susceptible = population - initial_exposed - initial_asymptomatic - initial_infected - \
                              initial_quarantine - initial_hospitalized - initial_uci - initial_recovered - \
                              initial_death

        initial_conditions = np.array([initial_susceptible, initial_exposed, initial_asymptomatic, initial_infected,
                                       initial_quarantine, initial_hospitalized, initial_uci, initial_recovered,
                                       initial_death])

        model_seaichurd = CovidSeaichurD()
        data, time = model_seaichurd.model(initial_conditions=initial_conditions,
                                           duration=duration, epidemiological_parameters=epidemiological_parameters)
        ds_dt = data[:, 0]
        de_dt = data[:, 1]
        da_dt = data[:, 2]
        di_dt = data[:, 3]
        dc_dt = data[:, 4]
        dh_dt = data[:, 5]
        du_dt = data[:, 6]
        dr_dt = data[:, 7]
        dd_dt = data[:, 8]
        time = np.around(time, decimals=2)

        return {'susceptible': ds_dt.tolist(),
                'exposed': de_dt.tolist(),
                'asymptomatic': da_dt.tolist(),
                'infected': di_dt.tolist(),
                'quarantine': dc_dt.tolist(),
                'hospitalized': dh_dt.tolist(),
                'uci': du_dt.tolist(),
                'recovered': dr_dt.tolist(),
                'death': dd_dt.tolist(),
                'time': time.tolist()}, HTTPStatus.OK
