from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from database import get_db
from order.cache import get_redis
from users.dependencies import get_current_user
from users.models import User
from order.schemas import OrderCreate, OrderRead, OrderUpdate
import order.services as services
from sqlalchemy.future import select
from order.models import Order

router = APIRouter(tags=["Orders"])


@router.post("/orders/", response_model=OrderRead)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await services.create_order(db, current_user.id, order_data)


@router.get("/orders/{order_id}/", response_model=OrderRead)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)):
    order = await services.get_order(db, redis, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.patch("/orders/{order_id}/", response_model=OrderRead)
async def update_order(order_id: UUID, update_data: OrderUpdate, db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)):
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await services.update_order(db, redis, order, update_data)
    return updated_order


@router.get("/orders/user/{user_id}/", response_model=list[OrderRead])
async def get_user_orders(user_id: int, db: AsyncSession = Depends(get_db)):
    return await services.get_user_orders(db, user_id)