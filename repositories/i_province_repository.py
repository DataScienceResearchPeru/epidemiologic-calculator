from abc import ABC, abstractmethod
from entities.province import Province


class IProvinceRepository(ABC):

    @abstractmethod
    def add(self, province: Province):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_department(self, department_id: int):
        pass
