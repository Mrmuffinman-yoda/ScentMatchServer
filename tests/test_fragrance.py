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
    fragrance_data = {
        "id": 123,
        "name": "DB Fragrance",
        "description": "A fragrance from the DB.",
        "slug": "db-fragrance",
        "image_url": "http://example.com/db-image.png",
    }
    insert_fragrance(**fragrance_data)
    response = client.get("/fragrance/?slug=db-fragrance")
    assert response.status_code == 200
    assert response.json() == fragrance_data


def test_get_fragrance_data_not_found_db():
    response = client.get("/fragrance/?slug=does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Fragrance not found"
