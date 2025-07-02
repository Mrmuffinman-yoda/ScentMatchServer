import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.User import UserORM
from app.utils.db_conn import SessionLocal

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the ScentMatch API!"}


def insert_user(**kwargs):
    db = SessionLocal()
    user = UserORM(**kwargs)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def test_get_user_data_found():
    user_data = {
        "id": 3,
        "username": "muffin",
        "email": "muffin@example.com",
    }
    insert_user(**user_data)
    response = client.get("/user/3")
    assert response.status_code == 200
    assert response.json() == user_data


def test_get_user_data_not_found():
    response = client.get("/user/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
