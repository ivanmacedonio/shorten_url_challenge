import datetime
from fastapi import HTTPException
from uuid import UUID
from jose import JWTError, jwt, ExpiredSignatureError
from app.domain.ports.input.token_service_port import TokenServicePort
from app.domain.configs.dependencies import JWT_SECRET_KEY, JWT_EXPIRATION_TIME
from app.domain.utils.singleton_wrapper import singleton_wrapper

@singleton_wrapper
class JWTService(TokenServicePort):
    def __init__(self):
        self.secret_key: str = JWT_SECRET_KEY
        self.algorithm: str = "HS256"
        self.expiration_time_in_minutes = int(JWT_EXPIRATION_TIME)
    
    def create_access_token(self, subject: UUID) -> str:
        expiration_in_datetime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=self.expiration_time_in_minutes)
        to_encode = {"sub": str(subject), "exp": expiration_in_datetime}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_access_token(self, token: str) -> str:
        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            subject = decoded_token.get("sub")
            
            if subject is None:
                raise JWTError("subject is missing")
            
            return subject
            
        except JWTError as jwte:
            raise HTTPException(status_code=401, detail={
                "message": "invalid access token, please login again",
                "detail": str(jwte)
            })
        
        except ExpiredSignatureError as jwte:
            raise HTTPException(status_code=401, detail={
                "message": "current token is already expired",
                "detail": str(jwte)
            })
        