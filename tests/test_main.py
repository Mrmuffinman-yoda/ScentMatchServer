from fastapi.testclient import TestClient
from app.main import app  # Import FastAPI app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the ScentMatch API!"}



def test_fragrance_id():
    response = client.get("/fragrance/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Fragrance data for ID 1."}
