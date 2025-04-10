import json
from uuid import UUID
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from order.tasks.publisher import publish_new_order
from order.models import Order, OrderStatus
from order.schemas import OrderCreate, OrderRead, OrderUpdate


CACHE_TTL = 300


async def create_order(db: AsyncSession, user_id: int, order_data: OrderCreate) -> Order:
    order = Order(
        user_id=user_id,
        items=order_data.items,
        total_price=order_data.total_price,
        status=OrderStatus.PENDING,
        created_at=datetime.now(),
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    await publish_new_order(str(order.id))
    return order


async def get_order(db: AsyncSession, redis: Redis, order_id: UUID) -> Order | None:
    cached = await redis.get(f"order:{order_id}")
    if cached:
        order_data = json.loads(cached)
        return OrderRead(**order_data)

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if order:
        await cache_order(redis, order)

    return order


async def update_order(db: AsyncSession, redis: Redis, order: Order, update_data: OrderUpdate) -> Order:
    if update_data.status:
        order.status = update_data.status

    await db.commit()
    await db.refresh(order)

    await cache_order(redis, order)
    return order


async def get_user_orders(db: AsyncSession, user_id: int) -> list[Order]:
    result = await db.execute(select(Order).filter(Order.user_id == user_id))
    return result.scalars().all()


async def cache_order(redis: Redis, order: Order):
    key = f"order:{order.id}"
    value = OrderRead.model_validate(order).model_dump_json()
    await redis.setex(key, CACHE_TTL, value)
