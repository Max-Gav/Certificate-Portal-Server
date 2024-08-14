import aio_pika

from db.db import MongoConnector
from tools.rabbitmq.rabbitmq_manager import RabbitMQManager


async def on_message_received(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        print("Received message:", message.body)
        message_str = bytes.decode(message.body)
        certificate_id = message_str.split(sep=" ", maxsplit=1)[0]
        await MongoConnector().fs.upload_from_stream(filename=certificate_id, source=message.body)


class RabbitMQUtils:

    async def setup_consumer(self):
        channel = RabbitMQManager().channel
        await channel.set_qos(prefetch_count=100)

        queue = await channel.declare_queue(name="certificate_creation", durable=True)

        await queue.consume(on_message_received)
