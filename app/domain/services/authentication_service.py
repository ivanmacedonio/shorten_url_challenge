from fastapi import HTTPException
from fastapi.responses import JSONResponse
from passlib.hash import bcrypt
from app.domain.entities.user import UserAuthenticateDTO, PartialUserRetrieveDTO
from app.domain.ports.input.token_service_port import TokenServicePort
from app.domain.ports.output.repositories.user_repository_port import UserRepositoryPort
from app.domain.ports.input.authentication_service_port import AuthenticationServicePort
from app.domain.utils.singleton_wrapper import singleton_wrapper

@singleton_wrapper
class AuthenticationService(AuthenticationServicePort):
    def __init__(self, user_repository: UserRepositoryPort, jwt_service: TokenServicePort):
        self.repository = user_repository
        self.jwt_service = jwt_service
        
    def register(self, payload: UserAuthenticateDTO) -> dict:
        user_already_exists = self.repository.get_by_email(payload.email)
        if user_already_exists:
            raise HTTPException(status_code=400, detail=f'user with email {payload.email} already exists')
        
        commited_user = self.repository.create(payload)
        return JSONResponse(status_code=201, content={
                                "message": "user created successfully",
                                "user_id": str(commited_user.id),
                                "email": commited_user.email})

    def login(self, payload: UserAuthenticateDTO):
        db_user: PartialUserRetrieveDTO = self.repository.get_by_email(payload.email)
        if db_user is None or not bcrypt.verify(payload.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = self.jwt_service.create_access_token(db_user.id)
        return JSONResponse(status_code=200, content={
            "message": "user authenticated successfully",
            "access_token": token,
            "token_type": "Bearer"
        })
