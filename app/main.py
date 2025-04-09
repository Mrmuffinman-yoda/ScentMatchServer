# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from app.utils.request_logger import log_requests
import json

from app.utils.redis_adapter import RedisAdapter

from app.utils.db_conn import DBConnection
from app.models import User
import logging
from app.models import FragranceHouse

logging.basicConfig(level=logging.info)
logger = logging.getLogger("uvicorn")

############################## Setup ####################################
load_dotenv()
app = FastAPI()
app.middleware("http")(log_requests)
conn = DBConnection()
r = RedisAdapter()
#########################################################################


@app.get("/user/{user_id}")
async def get_user_data(user_id: int):

    cache_key = f"user_data_{user_id}"

    cached_data = r.get(cache_key)
    if cached_data:
        logging.info(f"Cache hit for key: {cache_key}")
        return json.loads(cached_data)
    
    logging.info(f"Cache miss for key: {cache_key}")
    
    try:

        user = conn.execute_single(
            "SELECT username, email FROM users WHERE id = %s", (user_id,)
        )

        if user:
            # Build image URL assuming image names are stored as username.png
            image_url = f"http://127.0.0.1:9000/scentmatch/{user[0]}.png"

            # Cache the result for 30 minutes

            c_user = User(
                id=user_id,
                username=user[0],
                email=user[1],
                image_url=image_url,
            )
            r.set(
                cache_key,
                c_user.model_dump_json(),
                expire=1800,
            )

            return c_user.model_dump()
        else:
            return {"error": "User not found"}

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
async def root():
    return {"message": "Welcome to the ScentMatch API!"}

###############################################################################################################################
@app.get("/fragrance/{fragrance_house}")
async def get_fragrance_data(fragrance_house: str):
    """Will fetch from the database, for now create a dummy data"""

    cache_key =f"fragrance_data_{fragrance_house}"
    cached_data = r.get(cache_key)
    if cached_data:
        # Log the cache hit
        logging.info(f"Cache hit for key: {cache_key}")
        return json.loads(cached_data)

    logging.info(f"Cache miss for key: {cache_key}")

    try:
        # Log the incoming parameter
        logging.info(f"Fetching fragrance data for: {fragrance_house}")

        # Execute the query with case-insensitive matching
        frag_house = conn.execute_single(
            "SELECT id, name, founded, country_of_origin, logo_url, website_url, description FROM fragrance_house WHERE name ILIKE %s",
            (fragrance_house,),
        )

        # Log the query result
        logging.warning(f"Fragrance data: {frag_house}")

        if frag_house:
            house = FragranceHouse(
                id=frag_house[0],
                name=frag_house[1],
                founded=frag_house[2],
                country_of_origin=frag_house[3],
                logo_url=frag_house[4],
                website_url=frag_house[5],
                description=frag_house[6],
            )

            r.set(
                cache_key,
                house.model_dump_json(),
                expire=1800,
            )

            return house.model_dump()
        else:
            logging.error(f"No fragrance house found for: {fragrance_house}")
            return {"error": "Fragrance house not found"}
    except Exception as e:
        logging.exception("Error fetching fragrance data")
        return {"error": str(e)}
