from fastapi import APIRouter, Depends, Request
from uuid import UUID
from app.domain.ports.input.user_service_port import UserServicePort
from app.adapters.input.api.injectables import inject_user_service
from app.adapters.input.api.middlewares import verify_and_save_token_middleware
from app.domain.utils.rate_limiter import limiter

router = APIRouter(
    dependencies=[Depends(verify_and_save_token_middleware)]
)

@router.get("/")
@limiter.limit("30/minute")
def get_all_users(request: Request, service: UserServicePort = Depends(inject_user_service)):
    return service.get_all()

@router.get("/{user_id}")
@limiter.limit("30/minute")
def get_user_by_id(request: Request, user_id: UUID, service: UserServicePort = Depends(inject_user_service)):
    return service.get_by_id(user_id)

@router.delete("/{user_id}")
@limiter.limit("30/minute")
def delete_user(request: Request, user_id: UUID, service: UserServicePort = Depends(inject_user_service)):
    request_user_id = request.state.request_user_id
    return service.delete(user_id=user_id, request_user_id=request_user_id)
