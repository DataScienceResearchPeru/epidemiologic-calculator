from abc import ABC, abstractmethod
from entities.department import Departament


class IDepartamentRepository(ABC):

    @abstractmethod
    def add(self, departament: Departament):
        pass

    @abstractmethod
    def find_all(self):
        pass
