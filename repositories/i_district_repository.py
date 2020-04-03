from abc import ABC, abstractmethod
from entities.district import District


class IDistrictRepository(ABC):

    @abstractmethod
    def add(self, district: District):
        pass

    @abstractmethod
    def find_all(self):
        pass
