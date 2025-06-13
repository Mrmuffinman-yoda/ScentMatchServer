from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

class FragranceHouse(BaseModel):
    id: int
    name: str
    slug: str
    founded: int
    country_of_origin: str
    website_url: str
    description: str

    class Config:
        orm_mode = True
        from_attributes = True


###### ORM models #####
Base = declarative_base()

class FragranceHouseORM(Base):
    __tablename__ = "fragrance_house"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    founded = Column(Integer, nullable=True)
    country_of_origin = Column(String(50), nullable=True)
    website_url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
