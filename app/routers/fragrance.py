from fastapi import APIRouter, Depends, HTTPException
from app.utils.db_conn import get_db
from app.models.Fragrance import Fragrance, FragranceORM, FragranceTopClonesORM
from app.utils.redis_adapter import RedisAdapter
import logging
from sqlalchemy.orm import Session

redis = RedisAdapter()
router = APIRouter()


@router.get("/fragrance/", response_model=Fragrance)
async def get_fragrance_data(slug: str, db: Session = Depends(get_db)):
    logging.info(slug)
    cache_key = f"fragrance_data_{slug}"

    def fetch_fragrance():
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
            # Return a dict with an error key so the outer logic can raise 404
            return {"error": "Fragrance not found"}

    try:
        result = redis.cache_or_set(cache_key, fetch_fragrance, expire=1800)
        if isinstance(result, str):
            import json

            result = json.loads(result)
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return Fragrance(**result)
    except HTTPException as exc:
        raise exc


# Endpoint to retrieve top three fragrances from any fragrance
# using its fragrance-id from the table fragrance-top-clones
# there should only be a max of three fragrances returned
# and they should be ordered by rank
@router.get("/fragrance/{fragrance_id}/top-clones", response_model=list[Fragrance])
def get_top_three(fragrance_id: int, db: Session = Depends(get_db)):
    try:
        top_clones = (
            db.query(FragranceTopClonesORM)
            .filter(FragranceTopClonesORM.fragrance_id == fragrance_id)
            .order_by(FragranceTopClonesORM.rank)
            .limit(3)
            .all()
        )
        if not top_clones:
            raise HTTPException(status_code=404, detail="No top clones found")

        clone_ids = [clone.clone_id for clone in top_clones]
        fragrances = db.query(FragranceORM).filter(FragranceORM.id.in_(clone_ids)).all()
        id_to_fragrance = {f.id: f for f in fragrances}
        ordered_fragrances = [
            id_to_fragrance[clone_id]
            for clone_id in clone_ids
            if clone_id in id_to_fragrance
        ]

        return [Fragrance.from_orm(f) for f in ordered_fragrances]
    except Exception as e:
        logging.exception("Error fetching top clones")
        raise HTTPException(status_code=500, detail=str(e))
