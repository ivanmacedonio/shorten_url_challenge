from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    urls = relationship("ShortenURL", back_populates="creator")


class ShortenURL(Base):
    __tablename__ = 'shortenurl'

    id = Column(String, primary_key=True)
    raw_url = Column(String, nullable=False)
    shorten_url = Column(String, nullable=False)
    created_by = Column(String, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    creator = relationship("User", back_populates="urls")
