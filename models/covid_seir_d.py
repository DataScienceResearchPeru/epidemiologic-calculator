import numpy as np
from scipy.integrate import odeint
from models.i_covid_19 import ICovid19

# Parametros Epidemiologicos
A1 = 0.415    # contagio de SUSCEPTIBLE con INFECTADO
A2 = 0.70     # Periodo latente
A3 = 0.05     # Recuperacion
A4 = 0.00     # Muerte


class CovidSeirD(ICovid19):

    def model(self, initial_conditions, duration):
        """
        POBLACIONES EPIDEMIOLOGICAS
        Susceptibles (S) : initial_conditions[0]
        Expuestos    (E) : initial_conditions[1]
        Infectados   (I) : initial_conditions[2]
        Recuperados  (R) : initial_conditions[3]
        Pob. Muertos (D) : initial_conditions[4]

        POBLACION EPIDEMIOLOGICA TOTAL
        population = S + E + I + R + D
        """
        population = initial_conditions[0] + initial_conditions[1] + initial_conditions[2] + initial_conditions[3] + \
                     initial_conditions[4]
        time = np.arange(0, duration, 0.01)

        def seird(x, t, a1, a2, a3, a4):
            """
            SISTEMA DE ECUACIONES
            dS/dt = -a1*(SI/N)
            dE/dt = +a1*(SI/N) - a2*E
            dI/dt = +a2*E - a3*I - a4*I
            dR/dt = a3*I
            dD/dt = a4*I
            """
            return np.array([-a1*x[0]*x[2]/population,
                             a1*x[0]*x[2]/population - a2*x[1],
                             a2*x[1] - a3*x[2] - a4*x[2],
                             a3*x[2],
                             a4*x[2]])

        return odeint(seird, initial_conditions, time, (A1, A2, A3, A4)), time
