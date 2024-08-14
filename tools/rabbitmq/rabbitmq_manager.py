import aio_pika
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection

from tools.singleton import Singleton


class RabbitMQManager(metaclass=Singleton):
    connection: AbstractRobustConnection = None
    channel: AbstractRobustChannel = None
    host: str = None

    def init(self, host: str):
        self.host = host

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.host)
        self.channel = await self.connection.channel()

    async def close(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
