from app.domain.ports.input.user_service_port import UserPort
from app.domain.ports.output.repositories.user_repository_port import UserRepositoryPort
from app.domain.entities.user import UserRetrieveDTO, UserCreateDTO
from app.domain.utils.singleton_wrapper import singleton_wrapper
from fastapi import HTTPException
from typing import Union
from pydantic import EmailStr

@singleton_wrapper
class UserService(UserPort):
    def __init__(self, repository: UserRepositoryPort):
        self.repository = repository

    def get_by_id(self, user_id: Union[str, int]) -> UserRetrieveDTO:
        db_user = self.repository.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail=f'user with ID {user_id} not found')

        return db_user

    def get_user_already_exists_by_email(self, user_email) -> bool:
        if not user_email:
            raise ValueError(f'{user_email} is an invalid value for user_email')

        return self.repository.get_user_already_exists_by_email(user_email)

    def create(self, payload: UserCreateDTO) -> dict:
        if not payload:
            raise HTTPException(status_code=400, detail="payload is required to create an user")

        user_already_exists = self.get_user_already_exists_by_email(payload.email)
        if user_already_exists:
            raise HTTPException(status_code=400, detail=f'user with email {payload.email} already exists')

        return self.repository.create(payload)
