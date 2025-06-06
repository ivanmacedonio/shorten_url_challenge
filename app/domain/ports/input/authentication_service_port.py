from abc import abstractmethod, ABC
from fastapi.responses import JSONResponse
from app.domain.entities.user import UserAuthenticateDTO
from app.domain.ports.input.token_service_port import TokenServicePort
from app.domain.ports.output.repositories.user_repository_port import UserRepositoryPort

class AuthenticationServicePort(ABC):
    
    @abstractmethod
    def __init__(self, user_repository: UserRepositoryPort, jwt_service: TokenServicePort):
        pass
    
    @abstractmethod
    def register(self, payload: UserAuthenticateDTO) -> JSONResponse:
        pass
    
    @abstractmethod
    def login(self, payload: UserAuthenticateDTO) -> JSONResponse:
        pass
    
    
     