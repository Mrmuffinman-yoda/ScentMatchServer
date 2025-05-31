# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from app.utils.request_logger import log_requests
from app.utils.redis_adapter import RedisAdapter
from app.routers import user, fragrance
import logging

logging.basicConfig(level=logging.info)
logger = logging.getLogger("uvicorn")

############################## Setup ####################################
load_dotenv()
app = FastAPI()
app.middleware("http")(log_requests)
redis = RedisAdapter()
###########################Individual routers############################

app.include_router(user.router)
app.include_router(fragrance.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the ScentMatch API!"}
