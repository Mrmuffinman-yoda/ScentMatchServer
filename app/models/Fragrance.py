from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


class Fragrance(BaseModel):
    id: int
    name: str
    description : str
    slug: str

    class Config:
        orm_mode = True
        from_attributes = True


class FragranceTopClones(BaseModel):
    id: int
    fragrance_id : int
    clone_id : int
    rank : int


class FragranceImages(BaseModel):
    id: int
    slug: str
    image_count: int

    class Config:
        orm_mode = True
        from_attributes = True


class FragranceAccord(BaseModel):
    id: int
    slug: str
    accord: str
    percentage: int
    class Config:
        orm_mode = True
        from_attributes = True


class TopFragrance(BaseModel):
    id: int
    fragrance_id: int
    rank: int


###### ORM models #####
Base = declarative_base()

class FragranceORM(Base):
    __tablename__ = "fragrance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    slug = Column(String(50), nullable=False)
class FragranceTopClonesORM(Base):
    __tablename__ = "fragrance_top_clones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fragrance_id = Column(Integer, ForeignKey("fragrance.id"), nullable=False)
    clone_id = Column(Integer, ForeignKey("fragrance.id"), nullable=False)
    rank = Column(Integer, nullable=False)


class FragranceImagesORM(Base):
    __tablename__ = "fragrance_images"
    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(50), nullable=False)
    image_count = Column(Integer, nullable=False)

class FragranceAccordORM(Base):
    __tablename__ = "fragrance_accords"
    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(50), nullable=False)
    accord = Column(String(50), nullable=False)
    percentage = Column(Integer, nullable=False)


class TopFragranceORM(Base):
    __tablename__ = "top_fragrance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fragrance_id = Column(Integer, ForeignKey("fragrance.id"), nullable=False)
    rank = Column(Integer, nullable=False)