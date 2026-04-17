"""
Promotion schemas.
"""

from pydantic import BaseModel
from typing import Optional


class PromotionCreate(BaseModel):
    name: str
    code: str
    discount_type: str = "percentage"  # percentage | fixed
    discount_value: float
    start_date: str
    end_date: str
    status: str = "active"  # active | expired | scheduled


class PromotionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None


class PromotionResponse(BaseModel):
    id: str
    name: str
    code: str
    discount_type: str
    discount_value: float
    start_date: str
    end_date: str
    status: str
