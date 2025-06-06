from pydantic import BaseModel, PastDatetime, AnyHttpUrl
from typing import Optional
from uuid import UUID

class URLRetrieveDTO(BaseModel):
    raw_url: AnyHttpUrl
    shortened_url: str
    created_by: UUID
    created_at: PastDatetime
    deleted: bool
    
    def to_dict(self):
        return {
            "raw_url": str(self.raw_url),
            "shorten_url": self.shortened_url,
            "created_by": str(self.created_by),
            "created_at": str(self.created_at),
            "deleted": self.deleted
        }
        
class URLPartialRetrieveDTO(BaseModel):
    id: UUID
    shortened_url: str
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "shorten_url": self.shortened_url
        }

class URLCreateDTO(BaseModel):
    raw_url: AnyHttpUrl
    
    def to_dict(self): 
        return {
            "raw_url": str(self.raw_url),
        }
