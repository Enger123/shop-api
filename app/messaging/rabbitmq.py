from aio_pika.abc import AbstractChannel, AbstractRobustConnection, AbstractExchange
import aio_pika
from ..core.config import settings
import json

async def connect_rabbitmq() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(url=settings.RABBITMQ_URL)

async def declare_orders_exchange(channel: AbstractChannel):
    return await channel.declare_exchange(name=settings.ORDER_EXCHANGE, durable=True)

async def declare_notifications_queue(channel: AbstractChannel, exchange):
    queue = await channel.declare_queue(settings.NOTIFICATIONS_QUEUE, durable=True)
    await queue.bind(exchange, settings.ORDER_ROUTING_KEY)
    return queue

async def event_publish_json(exchange: AbstractExchange, routing_key: str, data: dict):
    message = aio_pika.Message(json.dumps(data).encode())
    await exchange.publish(message, routing_key)


