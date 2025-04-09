from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    image_url: str
