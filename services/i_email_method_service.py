from abc import ABC, abstractmethod


class IEmailMethodService(ABC):

    @abstractmethod
    def send_message(self, data_message: dict):
        pass
