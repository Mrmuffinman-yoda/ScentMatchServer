import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.db_conn import get_db
from app.models.User import User as UserModel, UserORM
from app.utils.redis_adapter import RedisAdapter

redis = RedisAdapter()
router = APIRouter()


@router.get("/user/{user_id}", response_model=UserModel)
async def get_user_data(user_id: int, db: Session = Depends(get_db)):
    cache_key = f"user_data_{user_id}"

    def fetch_user():
        try:
            user_orm = db.query(UserORM).filter(UserORM.id == user_id).first()
            if user_orm:
                user_dict = {
                    "id": user_orm.id,
                    "username": user_orm.username,
                    "email": user_orm.email,
                }
                return user_dict
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except HTTPException as e:
            raise
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
