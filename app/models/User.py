from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, Field

Base = declarative_base()


class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(
        String(100), nullable=False
    )  # We need to hash incoming password with BCRYPT standard


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    id: int
    username: str
    session_token: str
