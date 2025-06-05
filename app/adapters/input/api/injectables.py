from fastapi import Depends
from app.domain.services.database_service import DatabaseService
from app.domain.services.user_service import UserService
from app.domain.ports.input.user_service_port import UserServicePort
from app.adapters.output.repositories.user_repository_adapter import UserRepositoryAdapter
from app.domain.ports.output.repositories.user_repository_port import UserRepositoryPort
from app.domain.services.authentication_service import AuthenticationService
from app.domain.ports.input.authentication_service_port import AuthenticationServicePort
from app.domain.services.jwt_service import JWTService    
from app.domain.ports.input.token_service_port import TokenServicePort

def inject_database_service():
    return DatabaseService()

def inject_user_repository(db_service: DatabaseService = Depends(inject_database_service)) -> DatabaseService:
    return UserRepositoryAdapter(db_service=db_service)

def inject_user_service(repository: UserRepositoryPort = Depends(inject_user_repository)) -> UserServicePort:
    return UserService(repository=repository)

def inject_jwt_service() -> TokenServicePort:
    return JWTService()

def inject_authentication_service(jwt_service: TokenServicePort = Depends(inject_jwt_service),
                                  repository: UserRepositoryPort = Depends(inject_user_repository) ) -> AuthenticationServicePort:
    return AuthenticationService(jwt_service=jwt_service, user_repository=repository)
