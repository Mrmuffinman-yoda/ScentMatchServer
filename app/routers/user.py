import logging
from fastapi import APIRouter, HTTPException, Depends, Form, Header, Query
from sqlalchemy.orm import Session
from app.utils.db_conn import get_db
from app.models.User import User as UserModel, UserORM, LoginResponse
from app.utils.redis_adapter import RedisAdapter
import bcrypt
import secrets
import json
from app.constants import Timeouts, HTTPStatus

redis = RedisAdapter()
router = APIRouter()


@router.get("/user/{user_id}", response_model=UserModel)
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
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="User not found"
                )
        except Exception as e:
            logging.exception("Error fetching user data")
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
            )

    try:
        result = redis.cache_or_set(cache_key, fetch_user, expire=Timeouts.REDIS_CACHE)
        if isinstance(result, str):
            import json

            result = json.loads(result)
        # If result is an error dict, raise HTTPException
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=result["error"]
            )
        return UserModel(**result)
    except HTTPException as exc:
        raise exc


def get_user(data) -> str:
    return data.username


async def get_user_from_data(email: str, db: Session):
    """Get user from database using username and password to check for existence"""
    user_data = db.query(UserORM).filter(UserORM.email == email).first()
    if user_data:
        return user_data
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Account not found"
        )


@router.post("/user/login", response_model=LoginResponse)
async def get_user_login(
    email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user_data = await get_user_from_data(email, db)

    hashed_password = user_data.password

    if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        # make session token and save to redis
        session_token = secrets.token_urlsafe(32)

        cache_key = f"session:{session_token}"

        expiry = Timeouts.SESSION_TOKEN

        redis.cache_or_set(
            cache_key, expire=expiry, fetch_func=lambda: get_user(user_data)
        )

        # Pass the required arguments directly to the LoginResponse constructor
        return LoginResponse(
            id=user_data.id,
            username=user_data.username,
            session_token=session_token,
            expiry=expiry,
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/user-session")
async def get_user_from_session(
    session_token: str = Header(...), db: Session = Depends(get_db)
):
    """Get user data from session token stored in Redis cache"""
    cache_key = f"session:{session_token}"

    try:
        # Try to get user data from Redis cache
        cached_data = redis.get(cache_key)

        if cached_data:
            print("cache hit")
            # Return only the username as requested - simple JSON response
            return {"username": cached_data}
        else:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid or expired session token",
            )
    except Exception as e:
        logging.exception("Error retrieving user from session")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
