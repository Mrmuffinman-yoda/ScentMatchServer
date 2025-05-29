from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


class Fragrance(BaseModel):
    id: int
    name: str
    description : str
    slug : str
    image_url: str

class FragranceTopClones(BaseModel):
    id: int
    fragrance_id : int
    clone_id : int
    rank : int

###### ORM models #####
Base = declarative_base()

class FragranceORM(Base):
    __tablename__ = "fragrance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    slug = Column(String(50), nullable=False)
    image_url = Column("imageurl", String)  # <-- Fix here

class FragranceTopClonesORM(Base):
    __tablename__ = "fragrance_top_clones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fragrance_id = Column(Integer, ForeignKey("fragrance.id"), nullable=False)
    clone_id = Column(Integer, ForeignKey("fragrance.id"), nullable=False)
    rank = Column(Integer, nullable=False)