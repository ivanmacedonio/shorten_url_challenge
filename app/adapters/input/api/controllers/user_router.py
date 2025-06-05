from fastapi import APIRouter, Depends
from app.domain.ports.input.user_service_port import UserServicePort
from app.adapters.input.api.injectables import inject_user_service
from app.adapters.input.api.middlewares import verify_token_middleware
from uuid import UUID

router = APIRouter(
    dependencies=[Depends(verify_token_middleware)]
)

@router.get("/")
def get_all_users(service: UserServicePort = Depends(inject_user_service)):
    return service.get_all()

@router.get("/{user_id}")
def get_user_by_id(user_id: UUID, service: UserServicePort = Depends(inject_user_service)):
    return service.get_by_id(user_id)

@router.delete("/{user_id}")
def delete_user(user_id: UUID, service: UserServicePort = Depends(inject_user_service)):
    return service.delete(user_id)
