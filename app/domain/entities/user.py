from pydantic import BaseModel, EmailStr, PastDatetime

class UserRetrieveDTO(BaseModel):
    email: EmailStr
    created_at: PastDatetime
    deleted: bool
    urls: list

class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str