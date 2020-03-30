from abc import ABC, abstractmethod


class ICovid19(ABC):

    @abstractmethod
    def model(self, initial_conditions, duration, epidemiological_parameters):
        pass
