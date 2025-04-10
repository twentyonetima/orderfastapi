import aio_pika
import json
from config import RABBITMQ_URL

async def publish_new_order(order_id: str):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue("order_queue", durable=True)
        message_body = json.dumps({"order_id": order_id}).encode()
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body),
            routing_key="order_queue",
        )