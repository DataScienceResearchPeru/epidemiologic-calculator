import numpy as np
from scipy.integrate import odeint
from models.i_covid_19 import ICovid19

# Parametros Epidemiologicos
"""
A1 = 0.50  # contagio de SUSCEPTIBLE por un Infectado  [1/T]
A2 = 0.28  # contagio de SUSCEPTIBLE por un Asintomatico  [1/T] ( 12.5 dias )

A3 = 0.35  # Periodo Latente de un Asintomatico [1/T] (5 dias)
A4 = 0.40  # Periodo Latente de un Infectado [1/T] (5 dias)
A5 = 0.20  # Periodo Latente de Asintomatico para ser un Infectado [1/T] (5 dias)

A6 = 0.35  # Transicion de uno en Cuarentena a Infectado [1/T]
A7 = 0.50  # Contagio de Susceptibles-Cuarentena por un Asintomatico [1/T]
A8 = 0.15  # Hospitalizado trasladado a UCI [1/T]
A9 = 0.30  # Transicion de un Infectado a Hospitalizado [1/T]

QQ = 0.0  # Estado de CUARENTENA

R1 = 0.20  # Recuperacion de un Asintomatico [1/T]  (30 dias)
R2 = 0.15  # Recuperacion de un Infectado [1/T]  (40 dias)
R3 = 0.07  # Recuperacion de un Hospitalizado [1/T]  (40 dias)
R4 = 0.03  # Recuperacion de un UCI [1/T]  (20 dias)

D1 = 0.001  # Muerte de un Infectado [1/T]
D2 = 0.002  # Muerte de un Hospitalizado [1/T]
D3 = 0.005  # Muerte de un UCI [1/T]
"""


class CovidSeaichurD(ICovid19):
    def model(self, initial_conditions, duration, epidemiological_parameters=dict(A1=0.50, A2=0.28, A3=0.35, A4=0.40,
                                                                                  A5=0.20, A6=0.35, A7=0.50, A8=0.15,
                                                                                  A9=0.30, QQ=0.0, R1=0.20, R2=0.15,
                                                                                  R3=0.07, R4=0.03, D1=0.001, D2=0.002,
                                                                                  D3=0.005)):
        """
        POBLACIONES EPIDEMIOLOGICAS
        Susceptibles   (S) : initial_conditions[0]
        Expuestos      (E) : initial_conditions[1]
        Asintomatico   (A) : initial_conditions[2]
        Infectados     (I) : initial_conditions[3]
        Cuarentena     (C) : initial_conditions[4]
        Hospitalizados (H) : initial_conditions[5]
        UCI - Hospital (U) : initial_conditions[6]
        Recuperados    (R) : initial_conditions[7]
        Pob. Muertos   (D) : initial_conditions[8]

        POBLACION EPIDEMIOLOGICA TOTAL
        population = S + E + A + I + C + H + U + R + D
        """
        A1 = epidemiological_parameters["A1"]
        A2 = epidemiological_parameters["A2"]
        A3 = epidemiological_parameters["A3"]
        A4 = epidemiological_parameters["A4"]
        A5 = epidemiological_parameters["A5"]
        A6 = epidemiological_parameters["A6"]
        A7 = epidemiological_parameters["A7"]
        A8 = epidemiological_parameters["A8"]
        A9 = epidemiological_parameters["A9"]
        QQ = epidemiological_parameters["QQ"]
        R1 = epidemiological_parameters["R1"]
        R2 = epidemiological_parameters["R2"]
        R3 = epidemiological_parameters["R3"]
        R4 = epidemiological_parameters["R4"]
        D1 = epidemiological_parameters["D1"]
        D2 = epidemiological_parameters["D2"]
        D3 = epidemiological_parameters["D3"]

        population = initial_conditions[0] + initial_conditions[1] + initial_conditions[2] + initial_conditions[3] + \
                     initial_conditions[4] + initial_conditions[5] + initial_conditions[6] + initial_conditions[7] + \
                     initial_conditions[8]
        time = np.arange(0, duration, 1)

        def seaichurd(x, t, a1, a2, a3, a4, a5, a6, a7, a8, a9, r1, r2, r3, r4, qq, d1, d2, d3):
            """
            SISTEMA DE ECUACIONES
            #  dS/dt = -a1*(SI/N) - a2*(SA/N) - qq*S                        S[0]
            #  dE/dt = +a1*(SI/N) + a2*(SA/N) - a3*E - a4*E + a7*(CA/N)     E[1]
            #  dA/dt = +a3*E - a5*A - r1*A                                  A[2]
            #  dI/dt = +a4*E + a5*A - r2*I - d1*I - a9*I                    I[3]
            #  dC/dt = +qq*S - a6*C - a7*(CA/N)                             C[4]
            #  dH/dt = +a6*C - a8*H - d2*H + a9*I - r3*H + r4*U             H[5]
            #  dU/dt = +a8*H - d3*U - r4*U                                  U[6]
            #  dR/dt = r1*A + r2*I + r3*H                                   R[7]
            #  dD/dt = d1*I + d2*H + d3*U                                   D[8]
            """
            return np.array([-a1 * x[0] * x[3] / population - a2 * x[0] * x[2] / population - qq * x[0],
                             +a1 * x[0] * x[3] / population + a2 * x[0] * x[2] / population - a3 * x[1] - a4 * x[
                                 1] + a7 * x[4] * x[2] / population,
                             +a3 * x[1] - a5 * x[2] - r1 * x[2],
                             +a4 * x[1] + a5 * x[2] - r2 * x[2] - d1 * x[3] - a9 * x[3],
                             +qq * x[0] - a6 * x[4] - a7 * x[4] * x[2] / population,
                             +a6 * x[4] - a8 * x[5] - d2 * x[5] + a9 * x[3] - r3 * x[5] + r4 * x[6],
                             +a8 * x[5] - d3 * x[6] - r4 * x[6],
                             +r1 * x[2] + r2 * x[3] + r3 * x[5],
                             +d1 * x[3] + d2 * x[5] + d3 * x[6]])

        return odeint(seaichurd, initial_conditions, time,
                      (A1, A2, A3, A4, A5, A6, A7, A8, A9, R1, R2, R3, R4, QQ, D1, D2, D3)), \
               time
