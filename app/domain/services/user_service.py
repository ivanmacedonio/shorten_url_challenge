from app.domain.ports.input.user_service_port import UserServicePort
from app.domain.ports.output.repositories.user_repository_port import UserRepositoryPort
from app.domain.entities.user import UserRetrieveDTO
from app.domain.utils.singleton_wrapper import singleton_wrapper
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from uuid import UUID

@singleton_wrapper
class UserService(UserServicePort):
    def __init__(self, repository: UserRepositoryPort):
        self.repository = repository
        
    def get_all(self) -> list:
        users_list = self.repository.get_all()
        return JSONResponse(
            status_code = 200, 
            content = {"results": [user.to_dict() for user in users_list]}
        )

    def get_by_id(self, user_id: UUID) -> UserRetrieveDTO:
        db_user = self.repository.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail=f'user with ID {user_id} not found')

        return JSONResponse(status_code=200, content={
                "id": str(db_user.id),
                "email": db_user.email,
                "password": db_user.password,
                "created_at": str(db_user.created_at),
                "deleted": db_user.deleted,
                "shortened_urls": [] #TODO: Add the shortened URLS
            })
    
    def delete(self, user_id: UUID):
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        updated_user = self.repository.delete(user_id)
        if not updated_user:
            raise HTTPException(status_code=404, detail=f'user with id {user_id} not found or was already deleted')
        
        return JSONResponse(
                status_code=200,
                content={
                    "message": "user deleted successfully",
                    "user_id": str(updated_user.id)
                }
            )