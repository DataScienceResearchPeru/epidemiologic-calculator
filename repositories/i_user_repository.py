from abc import ABC, abstractmethod
from entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def get_user_by_email(self, email: str):
        pass
