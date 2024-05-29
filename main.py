import asyncio
import os
import uvicorn
import logging

from fastapi import APIRouter, FastAPI
from settings import Settings
from routers.certificate import certificate_router
from routers.user import user_router
from db.db import MongoConnector

app = FastAPI(title="Certmax")
settings = Settings()

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:     %(message)s')

def setup_routers():
    web_router = APIRouter()
    web_router.include_router(user_router.router)
    web_router.include_router(certificate_router.router)

    app.include_router(web_router)


@app.on_event("startup")
def startup_db_client():
    asyncio.get_event_loop().set_debug(True)
    MongoConnector().init(mongodb_uri=os.getenv("MONGODB_URI"), db_name=os.getenv("DB_NAME"))
    setup_routers()


@app.on_event("shutdown")
def shutdown_db_client():
    MongoConnector().close_connection()


if __name__ == "__main__":
    uvicorn.run(app=settings.app, host=settings.host, port=settings.port, reload=settings.reload)
