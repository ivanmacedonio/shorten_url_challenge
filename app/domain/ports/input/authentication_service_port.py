from abc import abstractmethod, ABC
from fastapi.responses import JSONResponse
from app.domain.entities.user import UserAuthenticateDTO

class AuthenticationServicePort(ABC):
    
    @abstractmethod
    def register(self, payload: UserAuthenticateDTO) -> JSONResponse:
        pass
    
    @abstractmethod
    def login(self, payload: UserAuthenticateDTO) -> JSONResponse:
        pass
    
    
     