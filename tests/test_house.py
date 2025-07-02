from fastapi.testclient import TestClient
from app.main import app
from app.models.Fragrance import Fragrance
from app.utils.db_conn import SessionLocal
import pytest
from app.models.FragranceHouse import FragranceHouseORM

client = TestClient(app)

def insert_fragrance(**kwargs):
    db = SessionLocal()
    fragrance_house = FragranceHouseORM(**kwargs)
    db.add(fragrance_house)
    db.commit()
    db.refresh(fragrance_house)
    db.close()
    return fragrance_house


def test_get_fragrance_house_data_found_db():

    house_data = {
        "id": 99,
        "name": "DB House",
        "slug": "db-house",
        "founded": 1990,
        "country_of_origin": "France",
        "website_url": "http://example.com/db-house",
        "description": "A fragrance house from the DB.",
    }

    insert_fragrance(**house_data)
    response = client.get("/house/?slug=db-house")
    assert response.status_code == 200
    assert response.json() == house_data

    response = client.get("/house/?house_id=99")
    assert response.status_code == 200
    assert response.json() == house_data