from fastapi.testclient import TestClient
from app.main import app
from app.models.Fragrance import Fragrance
from app.utils.db_conn import SessionLocal
import pytest
from app.models.Fragrance import FragranceORM

client = TestClient(app)

def insert_fragrance(**kwargs):
    db = SessionLocal()
    fragrance = FragranceORM(**kwargs)
    db.add(fragrance)
    db.commit()
    db.refresh(fragrance)
    db.close()
    return fragrance


def test_get_fragrance_data_found_db():
    """
    Test for retrieving fragrance data from the DB using slug or fragrance_id
    1. Insert a fragrance into the DB
    2. Retrieve it using slug
    3. Test response is 200 and matches the inserted data
    4. Retrieve it using fragrance_id
    5. Test response is 200 and matches the inserted data

    """
    fragrance_data = {
        "id": 123,
        "name": "DB Fragrance",
        "house_id": 1,
        "description": "A fragrance from the DB.",
        "slug": "db-fragrance",
    }
    insert_fragrance(**fragrance_data)
    response = client.get("/fragrance/?slug=db-fragrance")
    assert response.status_code == 200
    assert response.json() == fragrance_data

    response = client.get("/fragrance/?fragrance_id=123")
    assert response.status_code == 200
    assert response.json() == fragrance_data

def test_get_fragrance_data_not_found_db():
    response = client.get("/fragrance/?slug=does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Fragrance not found"
