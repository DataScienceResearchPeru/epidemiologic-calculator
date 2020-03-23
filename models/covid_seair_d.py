import numpy as np
from scipy.integrate import odeint
from models.i_covid_19 import ICovid19

# Parametros Epidemiologicos
A1 = 0.415  # contagio de SUSCEPTIBLE con INFECTADO
A2 = 0.90  # Periodo latente
A3 = 0.15  # Recuperacion
A4 = 0.00  # Muerte


class CovidSeairD(ICovid19):

    def model(self, initial_conditions, duration):
        """
        POBLACIONES EPIDEMIOLOGICAS
        Susceptibles  (S) : initial_conditions[0]
        Expuestos     (E) : initial_conditions[1]
        Asintomaticos (A) : initial_conditions[2]
        Infectados    (I) : initial_conditions[3]
        Recuperados   (R) : initial_conditions[4]
        Pob. Muertos  (D) : initial_conditions[5]

        POBLACION EPIDEMIOLOGICA TOTAL
        population = S + E + A + I + R + D
        """
        population = initial_conditions[0] + initial_conditions[1] + initial_conditions[2] + initial_conditions[3] + \
                     initial_conditions[4] + initial_conditions[5]
        time = np.arange(0, duration, 0.01)

        def seaird(x, t, a1, a2, a3, a4):
            return np.array([-a1 * x[0] * x[2] / population,
                             a1 * x[0] * x[2] / population - a2 * x[1],
                             a2 * x[1] - a3 * x[2] - a4 * x[2],
                             a3 * x[2],
                             a4 * x[2]])

        return odeint(seaird, initial_conditions, time, (A1, A2, A3, A4)), time
