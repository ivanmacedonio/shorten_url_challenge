from fastapi import APIRouter, Depends, Request
from uuid import UUID
from app.domain.ports.input.url_service_port import URLServicePort
from app.domain.entities.url import URLCreateDTO
from app.adapters.input.api.injectables import inject_url_service
from app.adapters.input.api.middlewares import verify_and_save_token_middleware
from app.domain.utils.rate_limiter import limiter

router = APIRouter(
    dependencies=[Depends(verify_and_save_token_middleware)]
)

public_router = APIRouter() # -> without jwt validation

@router.get("/")
@limiter.limit("30/minute")
def get_all_urls(request: Request, service: URLServicePort = Depends(inject_url_service)):
    return service.get_all()

@public_router.get("/{shortened_url}")
@limiter.limit("30/minute")
def redirect_by_shortened_id(request: Request, shortened_url: str, service: URLServicePort = Depends(inject_url_service)):
    return service.get_url_and_redirect(shortened_url=shortened_url)

@router.post("/")
@limiter.limit("10/minute")
def create_shortened_url(request: Request, payload: URLCreateDTO, service: URLServicePort = Depends(inject_url_service)):
    return service.save_url(payload=payload, current_user_id=request.state.request_user_id)

@router.delete("/{shortened_url}")
@limiter.limit("30/minute")
def delete_url(request: Request, shortened_url: str, service: URLServicePort = Depends(inject_url_service)):
    return service.delete(shortened_id=shortened_url)
