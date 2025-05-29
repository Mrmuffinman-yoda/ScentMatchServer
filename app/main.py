# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from app.utils.request_logger import log_requests
import json
from app.models.Fragrance import FragranceORM, Fragrance

from app.utils.redis_adapter import RedisAdapter
from sqlalchemy.orm import Session
from fastapi import Depends

from app.models.User import User as UserModel, UserORM
import logging
from app.models import Fragrance
from app.utils.db_conn import get_db

logging.basicConfig(level=logging.info)
logger = logging.getLogger("uvicorn")

############################## Setup ####################################
load_dotenv()
app = FastAPI()
app.middleware("http")(log_requests)
redis = RedisAdapter()
#########################################################################



from sqlalchemy import select
from app.models.User import User as UserModel, UserORM

from fastapi import HTTPException

@app.get("/user/{user_id}", response_model=UserModel)
async def get_user_data(user_id: int, db: Session = Depends(get_db)):
    cache_key = f"user_data_{user_id}"

    def fetch_user():
        try:
            user_orm = db.query(UserORM).filter(UserORM.id == user_id).first()
            if user_orm:
                image_url = f"http://127.0.0.1:9000/scentmatch/{user_orm.username}.png"
                user_dict = {
                    "id": user_orm.id,
                    "username": user_orm.username,
                    "email": user_orm.email,
                    "image_url": image_url,
                }
                return user_dict
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            logging.exception("Error fetching user data")
            raise HTTPException(status_code=500, detail=str(e))

    try:
        result = redis.cache_or_set(cache_key, fetch_user, expire=1800)
        if isinstance(result, str):
            import json
            result = json.loads(result)
        # If result is an error dict, raise HTTPException
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return UserModel(**result)
    except HTTPException as exc:
        raise exc

@app.get("/")
async def root():
    return {"message": "Welcome to the ScentMatch API!"}



@app.get("/fragrance/", response_model=Fragrance)
async def get_fragrance_data(slug: str, db: Session = Depends(get_db)):
    logging.info(slug)
    cache_key = f"fragrance_data_{slug}"

    def fetch_fragrance():
        try:
            fragrance_orm = db.query(FragranceORM).filter(FragranceORM.slug == slug).first()
            if fragrance_orm:
                fragrance = Fragrance(
                    id=fragrance_orm.id,
                    name=fragrance_orm.name,
                    description=fragrance_orm.description,
                    slug=fragrance_orm.slug,
                    image_url=fragrance_orm.image_url,
                )
                return fragrance.model_dump()
            else:
                return {"error": "Fragrance not found"}
        except Exception as e:
            logging.exception("Error fetching fragrance data")
            return {"error": str(e)}

    result = redis.cache_or_set(cache_key, fetch_fragrance, expire=1800)
    # If result is an error dict, return as is
    if isinstance(result, dict) and "error" in result:
        return result
    # If result is a string, try to decode to dict
    if isinstance(result, str):
        import json
        result = json.loads(result)
    return Fragrance(**result)