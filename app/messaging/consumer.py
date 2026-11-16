from aio_pika.abc import AbstractRobustConnection, AbstractConnection, AbstractIncomingMessage
import aio_pika
from app.core.config import settings
import json
from app.services.email import send_email


async def connect_rabbitmq() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.RABBITMQ_URL)

async def handle_notifications_event(message: AbstractIncomingMessage):
    async with message.process():
        event = json.loads(message.body.decode("utf-8"))
        print(event)

        general_body_response = ""
        for i, order_item in enumerate(event['items'], start=1):
            general_body_response += f"""\n{i})
            Product name: {order_item['product']} 
            Quantity: {order_item['quantity']}
            """
        
        await send_email(
            recipient=event['user_email'],
            subject=event['subject_for_email'],
            body=event['body_for_email'] + f": {general_body_response}"
            )
        

async def start_notifications_consume(connection: AbstractConnection):
    channel = await connection.channel()
    exchange = await channel.declare_exchange(settings.ORDER_EXCHANGE, durable=True)
    queue = await channel.declare_queue(settings.NOTIFICATIONS_QUEUE, durable=True)

    await queue.bind(exchange, settings.ORDER_ROUTING_KEY)
    await queue.consume(handle_notifications_event)

