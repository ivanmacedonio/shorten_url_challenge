from abc import ABC, abstractmethod
from app.domain.entities.user import UserRetrieveDTO, UserCreateDTO
from pydantic import EmailStr
from typing import Union

class UserPort(ABC):

    @abstractmethod
    def get_by_id(self, user_id: Union[str, int]) -> UserRetrieveDTO:
        pass

    @abstractmethod
    def get_user_already_exists_by_email(self, user_email: EmailStr) -> bool:
        pass

    @abstractmethod
    def create(self, payload):
        pass