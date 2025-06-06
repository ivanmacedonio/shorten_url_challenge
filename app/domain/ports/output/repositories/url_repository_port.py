from abc import abstractmethod, ABC
from typing import List
from uuid import UUID
from app.domain.ports.output.database_port import SQLDatabase
from app.domain.entities.url import URLCreateDTO, URLRetrieveDTO, URLPartialRetrieveDTO

class URLRepositoryPort(ABC):
    
    @abstractmethod
    def __init__(self, db_service: SQLDatabase):
        pass
    
    @abstractmethod
    def get_one(self, shortened_url: str) -> URLRetrieveDTO:
        pass
    
    @abstractmethod
    def get_all(self) -> List[URLRetrieveDTO]:
        pass
    
    @abstractmethod
    def create(self, payload: URLCreateDTO, current_user_id: UUID, shortened_url: str) -> URLPartialRetrieveDTO:
        pass
    
    @abstractmethod
    def delete_by_shortened_url(self, shortened_url: str) -> URLPartialRetrieveDTO:
        pass