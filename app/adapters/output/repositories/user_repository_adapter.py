from app.domain.ports.output.database_port import SQLDatabase
from app.domain.ports.output.repositories.user_repository_port import UserRepositoryPort
from app.domain.utils.singleton_wrapper import singleton_wrapper
from app.domain.entities.user import UserRetrieveDTO, UserCreateDTO
from app.domain.models.models import User
from fastapi.responses import JSONResponse
from typing import Union
from pydantic import EmailStr

@singleton_wrapper
class UserRepositoryAdapter(UserRepositoryPort):
    def __init__(self, db_service: SQLDatabase):
        self.db_service = db_service

    def get_by_id(self, user_id: Union[str, int]) -> UserRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            db_user = session.query(User).filter_by(id=user_id).first()
            return db_user

    def get_user_already_exists_by_email(self, user_email: EmailStr) -> bool:
        with self.db_service.session_scope_context() as session:
            users_with_same_email = session.query(User).filter_by(email=user_email).count()
            return users_with_same_email == 0 # Check if another user was used the payload email

    def create_user(self, payload: UserCreateDTO):
        with self.db_service.session_scope_context() as session:
            db_user = User(payload)
            session.add(db_user)
            return JSONResponse(status_code=201, content={"message": "user created successfully"})


