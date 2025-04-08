# main.py
from fastapi import FastAPI
import psycopg2

from app.models.FragranceHouse import FragranceHouse

app = FastAPI()

# Database connection details
DB_HOST = "postgres-db-test"
DB_NAME = "scentmatch_test_db"
DB_USER = "scentmatch_user"
DB_PASSWORD = "scentmatch_password"


@app.get("/user/{user_id}")
async def get_user_data(user_id: int):
    # Connect to PostgreSQL database
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cursor = conn.cursor()

        # Query user data
        cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            # Build image URL assuming image names are stored as username.png
            image_url = f"http://127.0.0.1:9000/scentmatch/{user[0]}.png"
            return {
                "user": {
                    "username": user[0],
                    "email": user[1],
                },
                "image_url": image_url,
            }
        else:
            return {"error": "User not found"}

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
async def root():
    return {"message": "Welcome to the ScentMatch API!"}


@app.get("/fragrance/{fragrance_house}")
async def get_fragrance_data(fragrance_house: str):
    """Will fetch from the database, for now create a dummy data"""

    # response = FragranceHouse(
    #     name=fragrance_house,
    #     founded=2016,
    #     country_of_origin="United Arab Emirates",
    #     logo_url="https://example.com/logo.jpg",
    #     website_url="https://example.com",
    #     description="Lattafa is a fragrance house known for its unique and captivating scents.",
    # )
    # return response.model_dump_json()

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cursor = conn.cursor()

        # Query fragrance data
        cursor.execute(
            "SELECT name, founded, country_of_origin, logo_url, website_url, description FROM fragrance_house WHERE name = %s",
            (fragrance_house,),
        )
        fragrance = cursor.fetchone()

        cursor.close()
        conn.close()

        if fragrance:
            return {
                "name": fragrance[0],
                "founded": fragrance[1],
                "country_of_origin": fragrance[2],
                "logo_url": fragrance[3],
                "website_url": fragrance[4],
                "description": fragrance[5],
            }
        else:
            return {"error": "Fragrance house not found"}
    except Exception as e:
        return {"error": str(e)}
