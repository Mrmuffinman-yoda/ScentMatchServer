from fastapi import Request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


async def log_requests(request: Request, call_next):
    # Log the incoming request
    body = await request.body()
    logger.info("------------------------Request-----------------------------")
    logger.info(f"Incoming request: {request.method} {request.url}")
    # logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Body: {body.decode('utf-8') if body else 'No body'}")

    # Process the request
    response = await call_next(request)

    # Log the outgoing response
    response_body = b"".join([chunk async for chunk in response.body_iterator])
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response body: {response_body.decode('utf-8')}")

    # Reassign the body iterator as an async generator
    async def response_body_generator():
        yield response_body

    response.body_iterator = response_body_generator()
    return response
