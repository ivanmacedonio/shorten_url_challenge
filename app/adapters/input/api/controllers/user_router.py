from fastapi import APIRouter, Depends
from app.domain.services.user_service import UserService
from app.adapters.input.api.injectables import get_user_service
from app.domain.entities.user import UserCreateDTO
from uuid import UUID

router = APIRouter()

@router.get("/")
def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all()

@router.get("/{user_id}")
def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):
    return service.get_by_id(user_id)

@router.post("/create")
def create_user(payload: UserCreateDTO, service: UserService = Depends(get_user_service)):
    return service.create(payload)

@router.delete("/{user_id}")
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    return service.delete(user_id)
