from fastapi import Depends, HTTPException, Header
from app.adapters.input.api.injectables import inject_jwt_service
from app.domain.ports.input.token_service_port import TokenServicePort

def verify_token_middleware(authorization: str = Header(default=..., alias="Authorization"), jwt_service: TokenServicePort = Depends(inject_jwt_service)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is required")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="the jwt provided is invalid")
    
    token = authorization.split(" ")[1]
    jwt_service.verify_access_token(token=token)
    