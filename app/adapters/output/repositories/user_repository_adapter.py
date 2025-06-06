from sqlalchemy import exists, select
from pydantic import EmailStr
from uuid import UUID
from typing import List
from passlib.hash import bcrypt
from app.domain.ports.output.database_port import SQLDatabase
from app.domain.ports.output.repositories.user_repository_port import UserRepositoryPort
from app.domain.utils.singleton_wrapper import singleton_wrapper
from app.domain.entities.user import UserRetrieveDTO, UserAuthenticateDTO, PartialUserRetrieveDTO
from app.domain.models.models import User
from app.domain.configs.logging import logger
from app.domain.utils.database_error_handler import handle_db_errors

@singleton_wrapper
class UserRepositoryAdapter(UserRepositoryPort):
    def __init__(self, db_service: SQLDatabase):
        self.db_service = db_service
    
    @handle_db_errors
    def get_all(self) -> List[UserRetrieveDTO]:
        with self.db_service.session_scope_context() as session:
            users_list: List[User] = session.query(User).filter_by(deleted = False)
            return [UserRetrieveDTO(
                    id = user.id,
                    email = user.email,
                    password = user.password,
                    created_at = user.created_at,
                    deleted = user.deleted,
                    shortened_urls = []
                ) for user in users_list]
    
    @handle_db_errors    
    def get_by_id(self, user_id: UUID) -> UserRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            db_user: User = session.query(User).filter_by(id=user_id, deleted=False).first()
            if not db_user: return
            
            return UserRetrieveDTO(
                id = user_id,
                email = db_user.email,
                password = db_user.password,
                created_at = db_user.created_at,
                deleted = db_user.deleted,
                shortened_urls = []
            )
    
    @handle_db_errors
    def create(self, payload: UserAuthenticateDTO) -> PartialUserRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            logger.info(f'Creating user with the next payload: {payload}')
            db_user = User(email=payload.email, password=bcrypt.hash(payload.password))
            session.add(db_user)
            logger.info(f'User {db_user.email} created successfully')
            session.flush()
            
            return PartialUserRetrieveDTO(
                id = db_user.id,
                email = db_user.email,
                password = db_user.password
            )
       
    @handle_db_errors     
    def delete(self, user_id: UUID) -> PartialUserRetrieveDTO: # soft delete
        with self.db_service.session_scope_context() as session:
            db_user: User = session.query(User).filter_by(id=user_id, deleted=False).first()
            if not db_user: return
            
            db_user.deleted = True
            logger.info(f'user {user_id} soft deleted successfully')
            return PartialUserRetrieveDTO(
                id = db_user.id,
                email = db_user.email,
                password=db_user.password
            )
    
    @handle_db_errors
    def get_user_already_exists_by_email(self, user_email: EmailStr) -> bool:
        with self.db_service.session_scope_context() as session:
            stmt = select(exists().where(User.email == user_email))
            result = session.execute(stmt).scalar()
            return result
    
    @handle_db_errors
    def get_by_email(self, user_email: EmailStr) -> PartialUserRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            db_user: User = session.query(User).filter_by(email=user_email, deleted=False).first()
            if not db_user: return

            return PartialUserRetrieveDTO(
                id=db_user.id,
                email=db_user.email,
                password=db_user.password
            )

            
            


