from fastapi import APIRouter, Depends
from app.domain.entities.user import UserAuthenticateDTO
from app.adapters.input.api.injectables import inject_authentication_service
from app.domain.ports.input.authentication_service_port import AuthenticationServicePort 

router = APIRouter()

@router.post("/login")
def login(payload: UserAuthenticateDTO, service: AuthenticationServicePort = Depends(inject_authentication_service)):
    return service.login(payload=payload)

@router.post("/register")
def register(payload: UserAuthenticateDTO, service: AuthenticationServicePort = Depends(inject_authentication_service)):
    return service.register(payload=payload)