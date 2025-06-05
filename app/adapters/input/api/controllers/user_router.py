from fastapi import APIRouter, Depends
from app.domain.services.user_service import UserService
from app.adapters.input.api.injectables import get_user_service
from app.domain.entities.user import UserCreateDTO

router = APIRouter()

@router.get("/get/{user_id}")
def get_user_by_id(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_by_id(user_id)

@router.post("/create")
def create_user(payload: UserCreateDTO, service: UserService = Depends(get_user_service)):
    return service.create(payload)