from fastapi.testclient import TestClient
from app.main import app  # Import FastAPI app
from app.models.FragranceHouse import FragranceHouse
import json

client = TestClient(app)


def test_fragrance_house():
    """This test will check if the fragrance house endpoint is working correctly.
    It should send the information for the fragrance house for example the name and when it was founded."""

    Lattafa = FragranceHouse(
        id=1,
        name="Lattafa",
        founded=1980,
        country_of_origin="United Arab Emirates",
        logo_url="https://example.com/logo.jpg",
        website_url="https://example.com",
        description="Lattafa is a fragrance house known for its unique and captivating scents.",
    )
    response = client.get("/fragrance/Lattafa")
    assert response.status_code == 200
    # Check if the response matches the expected data
    assert response.json() == json.loads(Lattafa.model_dump_json())
