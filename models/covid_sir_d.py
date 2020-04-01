import numpy as np
from scipy.integrate import odeint
from models.i_covid_19 import ICovid19

# Parametros Epidemiologicos
A1 = 0.415    # contagio de SUSCEPTIBLE con INFECTADO
A2 = 0.15     # Recuperacion
A3 = 0.00     # Muerte


class CovidSirD(ICovid19):

    def model(self, initial_conditions, duration, epidemiological_parameters=None):
        """
        POBLACIONES EPIDEMIOLOGICAS
        Susceptibles (S) : initial_conditions[0]
        Infectados   (I) : initial_conditions[1]
        Recuperados  (R) : initial_conditions[2]
        Pob. Muertos (D) : initial_conditions[3]

        POBLACION EPIDEMIOLOGICA TOTAL
        population = S + I + R + D
        """
        population = initial_conditions[0] + initial_conditions[1] + initial_conditions[2] + initial_conditions[3]
        time = np.arange(0, duration, 1)

        def sird(x, t, a1, a2, a3):
            """
            SISTEMA DE ECUACIONES
            dS/dt = -a1*(SI/population)
            dI/dt = +a1*(SI/population) - a2*I - a3*I
            dR/dt = a2*I
            dD/dt = a3*I
            """
            return np.array([-a1 * x[0] * x[1] / population,
                             a1 * x[0] * x[1] / population - a2 * x[1] + a3 * x[1],
                             a2 * x[1],
                             a3 * x[1]])

        return odeint(sird, initial_conditions, time, (A1, A2, A3)), time
