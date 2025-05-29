from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    # No image_url column; will be constructed in API
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    image_url: str
