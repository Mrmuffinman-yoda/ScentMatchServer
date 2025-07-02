from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.FragranceHouse import (
    FragranceHouse,
    FragranceHouseORM,
)
from app.utils.db_conn import get_db


from app.utils.redis_adapter import RedisAdapter
redis = RedisAdapter()
router = APIRouter()


@router.get("/house/", response_model=FragranceHouse)
def get_fragrance_house_data(
    db: Session = Depends(get_db), slug: str = None, house_id: int = None
):
    if slug is None and house_id is None:
        raise HTTPException(status_code=400, detail="Either slug or house_id must be provided.")

    if slug is not None:
        cache_key = f"fragrance_house_data_{slug}"

        def fetch_house():
            house_orm = db.query(FragranceHouseORM).filter(FragranceHouseORM.slug == slug).first()
            if house_orm:
                return FragranceHouse.from_orm(house_orm).dict()
            else:
                return {"error": "Fragrance house not found"}

        try:
            result = redis.cache_or_set(cache_key, fetch_house, expire=1800)
            if isinstance(result, str):
                import json
                result = json.loads(result)
            if isinstance(result, dict) and "error" in result:
                raise HTTPException(status_code=404, detail=result["error"])
            return FragranceHouse(**result)
        except HTTPException as exc:
            raise exc

    # Get by house_id
    house_orm = db.query(FragranceHouseORM).filter(FragranceHouseORM.id == house_id).first()
    if not house_orm:
        raise HTTPException(status_code=404, detail="Fragrance house not found")
    return FragranceHouse.from_orm(house_orm)