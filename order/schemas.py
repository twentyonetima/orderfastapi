from pydantic import BaseModel, ConfigDict
from typing import List, Any
from uuid import UUID
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"


class OrderCreate(BaseModel):
    items: List[Any]
    total_price: float


class OrderRead(BaseModel):
    id: UUID
    user_id: int
    items: List[Any]
    total_price: float
    status: OrderStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            UUID: lambda u: str(u),
            datetime: lambda dt: dt.isoformat()
        }
    )


class OrderUpdate(BaseModel):
    status: OrderStatus
