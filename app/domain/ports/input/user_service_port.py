from abc import ABC, abstractmethod
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
    def delete(self, user_id: UUID) -> JSONResponse: 
        pass