from fastapi import Depends
from app.domain.services.user_service import UserService
from app.adapters.output.repositories.user_repository_adapter import UserRepositoryAdapter
from app.domain.services.database_service import DatabaseService

def get_database_service():
    return DatabaseService()

def get_user_repository(db_service: DatabaseService = Depends(get_database_service)) -> DatabaseService:
    return UserRepositoryAdapter(db_service=db_service)

def get_user_service(repository: UserRepositoryAdapter = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repository)
