import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the ScentMatch API!"}

def test_get_user_data_found(monkeypatch):
    user_data = {
        "id": 1,
        "username": "muffin",
        "email": "muffin@example.com",
        "image_url": "http://127.0.0.1:9000/scentmatch/muffin.png"
    }
    def mock_cache_or_set(key, fetch_func, expire=None):
        return user_data
    monkeypatch.setattr("app.main.redis.cache_or_set", mock_cache_or_set)
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == user_data

def test_get_user_data_not_found(monkeypatch):
    def mock_cache_or_set(key, fetch_func, expire=None):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    monkeypatch.setattr("app.main.redis.cache_or_set", mock_cache_or_set)
    response = client.get("/user/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

