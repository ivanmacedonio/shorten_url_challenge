from app.domain.services.user_service import UserService
from app.adapters.output.repositories.user_repository_adapter import UserRepositoryAdapter

def get_user_repository() -> UserRepository:
    return UserRepositoryAdapter()

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repository)
