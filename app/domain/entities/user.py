from pydantic import BaseModel, EmailStr, PastDatetime
from uuid import UUID
from typing import Optional

class UserRetrieveDTO(BaseModel):
    id: Optional[UUID]
    email: EmailStr
    password: Optional[str]
    created_at: PastDatetime
    deleted: bool
    shortened_urls: list
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "password": self.password,
            "created_at": str(self.created_at),
            "deleted": self.deleted,
            "shortened_urls": self.shortened_urls
        }
    
class PartialUserRetrieveDTO(BaseModel):
    id: UUID
    email: EmailStr
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email
        }

class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str
    
    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password
        }
