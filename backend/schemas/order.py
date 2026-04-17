"""
Order schemas.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    total: float
    status: str = "pending"  # pending | processing | completed | refunded


class OrderStatusUpdate(BaseModel):
    status: str  # pending | processing | completed | refunded


class OrderResponse(BaseModel):
    id: str
    order_id: str   # e.g. #ORD-9932
    customer_name: str
    customer_email: str
    total: float
    status: str
    created_at: str


class OrderSummary(BaseModel):
    pending: int = 0
    processing: int = 0
    completed: int = 0
    refunded: int = 0
