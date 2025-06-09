from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


class TopFragrance(BaseModel):
    id: int
    fragrance_id: int
    rank: int

    class Config:
        orm_mode = True
        from_attributes = True


###### ORM models #####
Base = declarative_base()


class TopFragranceORM(Base):
    __tablename__ = "top_fragrances"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fragrance_id = Column(Integer, ForeignKey("fragrance.id"), nullable=False)
    rank = Column(Integer, nullable=False)
