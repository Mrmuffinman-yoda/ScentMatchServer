from fastapi import APIRouter, Depends, HTTPException
from app.utils.db_conn import get_db
from app.models.Fragrance import (
    Fragrance,
    FragranceORM,
    FragranceTopClonesORM,
    FragranceImagesORM,
    FragranceImages,
    FragranceAccordORM,
    FragranceAccord,
)
from app.models.TopFragrances import TopFragrance, TopFragranceORM
from app.utils.redis_adapter import RedisAdapter
import logging
from sqlalchemy.orm import Session
import app.utils.config as config
redis = RedisAdapter()
router = APIRouter()


# Get fragrance by slug
@router.get("/fragrance/", response_model=Fragrance)
async def get_fragrance_data(
    slug: str = None, fragrance_id: int = None, db: Session = Depends(get_db)
):
    if slug is None and fragrance_id is None:
        raise HTTPException(status_code=400, detail="Either slug or fragrance_id must be provided.")

    if slug is not None:
        logging.info(f"Get fragrance by slug: {slug}")
        cache_key = f"fragrance_data_{slug}"

        def fetch_fragrance():
            fragrance_orm = db.query(FragranceORM).filter(FragranceORM.slug == slug).first()
            if fragrance_orm:
                fragrance = Fragrance(
                    id=fragrance_orm.id,
                    name=fragrance_orm.name,
                    description=fragrance_orm.description,
                    slug=fragrance_orm.slug,
                )
                return fragrance.model_dump()
            else:
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

    # Get by fragrance_id
    logging.info(f"Get fragrance by id: {fragrance_id}")
    fragrance_orm = db.query(FragranceORM).filter(FragranceORM.id == fragrance_id).first()
    if not fragrance_orm:
        raise HTTPException(status_code=404, detail="Fragrance not found")
    return Fragrance(
        id=fragrance_orm.id,
        name=fragrance_orm.name,
        description=fragrance_orm.description,
        slug=fragrance_orm.slug,
    )


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
            id_to_fragrance[clone_id] for clone_id in clone_ids if clone_id in id_to_fragrance
        ]

        return [Fragrance.from_orm(f) for f in ordered_fragrances]
    except Exception as e:
        logging.exception("Error fetching top clones")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fragrance/{slug}/carousel", response_model=list[FragranceImages])
def get_fragrance_carousel(slug: str, db: Session = Depends(get_db)):
    try:
        images = db.query(FragranceImagesORM).filter(FragranceImagesORM.slug == slug).all()
        if not images:
            raise HTTPException(status_code=404, detail="No images found")

        return [FragranceImages.from_orm(img) for img in images]
    except Exception as e:
        logging.exception("Error fetching fragrance carousel")
        raise HTTPException(status_code=500, detail=str(e))


# With the fragrance slug as input, return the accords
@router.get("/fragrance/{slug}/accords", response_model=list[FragranceAccord])
def get_fragrance_accords(slug: str, db: Session = Depends(get_db)):
    try:
        accords = db.query(FragranceAccordORM).filter(FragranceAccordORM.slug == slug).all()
        if not accords:
            raise HTTPException(status_code=404, detail="No accords found")

        return [FragranceAccord.from_orm(accord) for accord in accords]
    except Exception as e:
        logging.exception("Error fetching fragrance accords")
        raise HTTPException(status_code=500, detail=str(e))


# endpoint to retrieve top three fragrances
@router.get("/fragrance/top-fragrances", response_model=list[TopFragrance])
def get_top_fragrances(db: Session = Depends(get_db)):
    try:
        top_fragrances = db.query(TopFragranceORM).order_by(TopFragranceORM.rank).limit(3).all()
        if not top_fragrances:
            raise HTTPException(status_code=404, detail="No top fragrances found")

        return [TopFragrance.from_orm(tf) for tf in top_fragrances]
    except Exception as e:
        logging.exception("Error fetching top fragrances")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to get fragrance page URL by id or slug
@router.get("/fragrance/page-url")
def get_fragrance_page_url(slug: str = None, fragrance_id: int = None, db: Session = Depends(get_db)):
    """
    Returns the URL of the fragrance page given a slug or id, in the format /info/{house_slug}/{fragrance_slug}
    """
    if slug is None and fragrance_id is None:
        raise HTTPException(status_code=400, detail="Either slug or fragrance_id must be provided.")

    if slug:
        fragrance_orm = db.query(FragranceORM).filter(FragranceORM.slug == slug).first()
    else:
        fragrance_orm = db.query(FragranceORM).filter(FragranceORM.id == fragrance_id).first()

    if not fragrance_orm:
        raise HTTPException(status_code=404, detail="Fragrance not found")

    # Get house_slug from fragrance ORM (via house_id)
    house_id = getattr(fragrance_orm, 'house_id', None)
    if not house_id:
        raise HTTPException(status_code=500, detail="Fragrance missing house_id")

    from app.models.FragranceHouse import FragranceHouseORM
    house_orm = db.query(FragranceHouseORM).filter(FragranceHouseORM.id == house_id).first()
    if not house_orm:
        raise HTTPException(status_code=404, detail="House not found")


    url = f"{config.BASE_URL}/info/{house_orm.slug}/{fragrance_orm.slug}"
    return {"url": url}

