from abc import abstractmethod, ABC
from uuid import UUID

class TokenServicePort(ABC):
    
    @abstractmethod
    def create_access_token(self, subject: UUID) -> str:
        pass
    
    @abstractmethod
    def verify_access_token(self, token: str) -> str:
        pass