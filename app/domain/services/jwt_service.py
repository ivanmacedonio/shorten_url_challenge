from app.domain.ports.input.token_service_port import TokenServicePort
from datetime import datetime, timedelta
from app.domain.configs.dependencies import JWT_SECRET_KEY
from uuid import UUID
from jose import JWTError, jwt

class JWTService(TokenServicePort):
    def __init__(self):
        self.secret_key = JWT_SECRET_KEY
        self.algorithm: str = "HS256"
        self.expiration_time_in_minutes: int = 60
    
    def create_access_token(self, subject: UUID) -> str:
        expiration_in_datetime = datetime.now() + timedelta(minutes=self.expiration_time_in_minutes)
        to_encode = {"sub": str(subject), "exp": expiration_in_datetime}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_access_token(self, token: str) -> str:
        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            subject = decoded_token.get("sub")
            
            if subject is None:
                raise JWTError("subject is missing")
            
        except JWTError:
            raise JWTError("invalid access token, please login again")
        