from pydantic import BaseModel, PastDatetime, AnyHttpUrl
from typing import Optional
from uuid import UUID

class URLRetrieveDTO(BaseModel):
    id: Optional[UUID]
    raw_url: AnyHttpUrl
    shorten_url: str
    created_by: UUID
    created_at: PastDatetime
    deleted: bool
    
    def to_dict(self):
        return {
            "id": self.id,
            "raw_url": self.raw_url,
            "shorten_url": self.shorten_url,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "deleted": self.deleted
        }
        
class URLPartialRetrieveDTO(BaseModel):
    id: UUID
    shorten_url: str
    
    def to_dict(self):
        return {
            "id": self.id,
            "shorten_url": self.shorten_url
        }

class URLCreateDTO(BaseModel):
    raw_url: AnyHttpUrl
    shorten_url: str
    created_by: UUID
    
    def to_dict(self): 
        return {
            "raw_url": self.raw_url,
            "shorten_url": self.shorten_url,
            "created_by": self.created_by
        }
