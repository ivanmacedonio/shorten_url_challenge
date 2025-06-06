from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities.url import URLCreateDTO
from fastapi.responses import JSONResponse, RedirectResponse
from app.domain.ports.output.repositories.url_repository_port import URLRepositoryPort

class URLServicePort(ABC):
    
    @abstractmethod
    def __init__(self, repository: URLRepositoryPort):
        pass
    
    @abstractmethod
    def save_url(self, payload: URLCreateDTO, current_user_id: UUID) -> JSONResponse:
        pass
    
    @abstractmethod
    def get_url_and_redirect(self, shortened_url: str) -> RedirectResponse:
        pass
    
    @abstractmethod
    def get_all(self) -> JSONResponse:
        pass
    
    @abstractmethod
    def delete(self, shortened_id: str) -> JSONResponse:
        pass