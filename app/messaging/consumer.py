from aio_pika.abc import AbstractRobustConnection, AbstractConnection, AbstractIncomingMessage
import aio_pika
from app.core.config import settings
import json


async def connect_rabbitmq() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.RABBITMQ_URL)

async def handle_notifications_event(message: AbstractIncomingMessage):
    async with message.process():
        event = json.loads(message.body.decode("utf-8"))
        print(event)

async def start_notifications_consume(connection: AbstractConnection):
    channel = await connection.channel()
    exchange = await channel.declare_exchange(settings.ORDER_EXCHANGE, durable=True)
    queue = await channel.declare_queue(settings.NOTIFICATIONS_QUEUE, durable=True)

    await queue.bind(exchange, settings.ORDER_ROUTING_KEY)
    await queue.consume(handle_notifications_event)

