from abc import ABC, abstractmethod
from entities.department import Department


class IDepartmentRepository(ABC):

    @abstractmethod
    def add(self, department: Department):
        pass

    @abstractmethod
    def find_all(self):
        pass
