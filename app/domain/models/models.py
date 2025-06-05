from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    deleted = Column(Boolean, default=False)

    urls = relationship("URL", back_populates="creator")
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "deleted": self.deleted
        }


class URL(Base):
    __tablename__ = 'urls'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_url = Column(String, nullable=False)
    shorten_url = Column(String(20), nullable=False, unique=True)
    created_by = Column(UUID, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    deleted = Column(Boolean, default=False)

    creator = relationship("User", back_populates="urls")
    
    def to_dict(self):
        return {
            "id": self.id,
            "raw_url": self.raw_url,
            "shorten_url": self.shorten_url,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "deleted": self.deleted
        }
