from abc import ABC, abstractmethod
from fastapi.responses import JSONResponse
from uuid import UUID
from app.domain.ports.output.repositories.user_repository_port import UserRepositoryPort

class UserServicePort(ABC):
    
    @abstractmethod
    def __init__(self, repository: UserRepositoryPort):
        pass
    
    @abstractmethod
    def get_all(self) -> JSONResponse:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> JSONResponse:
        pass

    @abstractmethod
    def delete(self, request_user_id: UUID, user_id: UUID) -> JSONResponse: 
        pass