import logging

from tools.singleton import Singleton
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorGridFSBucket


class MongoConnector(metaclass=Singleton):
    mongodb_uri: str = None
    db_name: str = None
    mongodb_client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None
    fs: AsyncIOMotorGridFSBucket = None

    def init(self, mongodb_uri, db_name) -> None:
        self.mongodb_uri = mongodb_uri
        self.db_name = db_name

        self.mongodb_client = AsyncIOMotorClient(mongodb_uri)
        logging.info("Established Connection with Mongodb")

        self.db = self.mongodb_client[self.db_name]
        logging.info("Accessing the database named: " + self.db_name)

        self.fs = AsyncIOMotorGridFSBucket(self.db)
        logging.info("Initialized GridFS")

    def close_connection(self):
        self.mongodb_client.close()
        logging.info("Closing Connection with Mongodb")
