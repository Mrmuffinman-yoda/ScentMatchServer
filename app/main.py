# main.py
from fastapi import FastAPI
import psycopg2

app = FastAPI()

# Database connection details
DB_HOST = "postgres-db"
DB_NAME = "scentmatch_db"
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
                "image_url": image_url
            }
        else:
            return {"error": "User not found"}
    
    except Exception as e:
        return {"error": str(e)}
