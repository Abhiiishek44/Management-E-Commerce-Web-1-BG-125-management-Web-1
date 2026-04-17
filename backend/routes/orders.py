"""
Order Routes — /api/orders
"""

from fastapi import APIRouter, Depends, Query
from controllers import order_controller
from schemas.order import OrderCreate, OrderStatusUpdate
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("/summary")
async def get_order_summary(_user: dict = Depends(get_current_user)):
    return await order_controller.get_order_summary()


@router.get("")
async def list_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(""),
    _user: dict = Depends(get_current_user),
):
    return await order_controller.list_orders(page, limit, status)


@router.get("/{order_id}")
async def get_order(order_id: str, _user: dict = Depends(get_current_user)):
    return await order_controller.get_order(order_id)


@router.post("")
async def create_order(data: OrderCreate, _user: dict = Depends(get_current_user)):
    return await order_controller.create_order(data)


@router.put("/{order_id}/status")
async def update_order_status(
    order_id: str, data: OrderStatusUpdate, _user: dict = Depends(get_current_user)
):
    return await order_controller.update_order_status(order_id, data)
