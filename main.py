import asyncio
import os
import uvicorn
import logging

from fastapi import APIRouter, FastAPI
from settings import Settings
from routers.certificate import certificate_router
from routers.user import user_router
from db.db import MongoConnector
from fastapi.middleware.cors import CORSMiddleware

from tools.rabbitmq.rabbitmq_manager import RabbitMQManager
from tools.rabbitmq.rabbitmq_utils import RabbitMQUtils

app = FastAPI(title="Certmax")
settings = Settings()

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:     %(message)s')

app.add_middleware(CORSMiddleware,
                   allow_origins=settings.allow_origins,
                   allow_credentials=settings.allow_credentials,
                   allow_methods=settings.allow_methods,
                   allow_headers=settings.allow_headers, )


def setup_routers():
    web_router = APIRouter()
    web_router.include_router(user_router.router)
    web_router.include_router(certificate_router.router)

    app.include_router(web_router)


@app.on_event("startup")
async def startup():
    asyncio.get_event_loop().set_debug(settings.is_dev)

    MongoConnector().init(mongodb_uri=os.getenv("MONGODB_URI"), db_name=os.getenv("DB_NAME"))

    setup_routers()

    RabbitMQManager().init(host=settings.rabbitmq_host)
    await RabbitMQManager().connect()
    await RabbitMQUtils().setup_consumer()


@app.on_event("shutdown")
async def shutdown():
    MongoConnector().close_connection()
    await RabbitMQManager().close()


if __name__ == "__main__":
    uvicorn.run(app=settings.app, host=settings.host, port=settings.port, reload=settings.reload)
