from abc import abstractmethod, ABC
from typing import List
from app.domain.ports.output.database_port import SQLDatabase
from app.domain.entities.url import URLCreateDTO, URLRetrieveDTO, URLPartialRetrieveDTO

class URLRepositoryPort(ABC):
    
    @abstractmethod
    def __init__(self, db_service: SQLDatabase):
        pass
    
    @abstractmethod
    def get(self, shortened_url: str) -> URLRetrieveDTO:
        pass
    
    @abstractmethod
    def get_all(self) -> List[URLPartialRetrieveDTO]:
        pass
    
    @abstractmethod
    def create(self, payload: URLCreateDTO) -> URLPartialRetrieveDTO:
        pass
    
    @abstractmethod
    def delete(self, shortened_url: str) -> URLPartialRetrieveDTO:
        pass