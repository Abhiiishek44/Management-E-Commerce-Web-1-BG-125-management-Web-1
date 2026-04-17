"""
Common schemas — pagination, response envelope.
"""

from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 1
    limit: int = 10


class PaginatedResponse(BaseModel):
    success: bool = True
    data: List[Any] = []
    total: int = 0
    page: int = 1
    limit: int = 10
    pages: int = 0


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: Optional[str] = None
