from pydantic import BaseModel


class FragranceHouse(BaseModel):
    name: str
    founded: int
    country_of_origin: str
    logo_url: str
    website_url: str
    description: str
