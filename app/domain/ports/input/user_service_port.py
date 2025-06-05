from abc import ABC, abstractmethod
from app.domain.entities.user import UserRetrieveDTO, UserCreateDTO
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from uuid import UUID

class UserServicePort(ABC):
    
    @abstractmethod
    def get_all(self) -> JSONResponse:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> JSONResponse:
        pass

    @abstractmethod
    def create(self, payload: UserCreateDTO) -> JSONResponse:
        pass
    
    @abstractmethod
    def delete(self, user_id: UUID) -> JSONResponse: 
        pass