from fastapi import APIRouter, Depends, Request
from app.domain.entities.user import UserAuthenticateDTO
from app.adapters.input.api.injectables import inject_authentication_service
from app.domain.ports.input.authentication_service_port import AuthenticationServicePort 
from app.domain.utils.rate_limiter import limiter

router = APIRouter()

@router.post("/login")
@limiter.limit("6/minute")
def login(request: Request, payload: UserAuthenticateDTO, service: AuthenticationServicePort = Depends(inject_authentication_service)):
    return service.login(payload=payload)

@router.post("/register")
@limiter.limit("6/hour")
def register(request: Request, payload: UserAuthenticateDTO, service: AuthenticationServicePort = Depends(inject_authentication_service)):
    return service.register(payload=payload)