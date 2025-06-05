from abc import ABC, abstractmethod
from pydantic import EmailStr
from uuid import UUID
from typing import List
from app.domain.entities.user import UserRetrieveDTO, UserAuthenticateDTO, PartialUserRetrieveDTO

class UserRepositoryPort(ABC):
    
    @abstractmethod
    def get_all(self) -> List[UserRetrieveDTO]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> UserRetrieveDTO:
        pass
    
    @abstractmethod
    def get_by_email(self, user_email: EmailStr) -> PartialUserRetrieveDTO:
        pass

    @abstractmethod
    def get_user_already_exists_by_email(self, email: EmailStr) -> bool:
        pass

    @abstractmethod
    def create(self, payload: UserAuthenticateDTO) -> PartialUserRetrieveDTO:
        pass
    
    @abstractmethod
    def delete(self, user_ud: UUID) -> PartialUserRetrieveDTO:
        pass