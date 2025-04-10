import asyncio
import aio_pika
import json
from config import RABBITMQ_URL
from order.tasks.task import process_order

async def consume():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("order_queue", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body)
                order_id = data["order_id"]
                process_order.delay(order_id)
                print(f"Data {data}")
                print(f"Order {order_id} sent to Celery")

if __name__ == "__main__":
    asyncio.run(consume())