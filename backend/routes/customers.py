"""
Customer Routes — /api/customers
"""

from fastapi import APIRouter, Depends, Query
from controllers import customer_controller
from schemas.customer import CustomerCreate, CustomerUpdate
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("")
async def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(""),
    _user: dict = Depends(get_current_user),
):
    return await customer_controller.list_customers(page, limit, search)


@router.get("/{customer_id}")
async def get_customer(customer_id: str, _user: dict = Depends(get_current_user)):
    return await customer_controller.get_customer(customer_id)


@router.post("")
async def create_customer(data: CustomerCreate, _user: dict = Depends(get_current_user)):
    return await customer_controller.create_customer(data)


@router.put("/{customer_id}")
async def update_customer(customer_id: str, data: CustomerUpdate, _user: dict = Depends(get_current_user)):
    return await customer_controller.update_customer(customer_id, data)


@router.delete("/{customer_id}")
async def delete_customer(customer_id: str, _user: dict = Depends(get_current_user)):
    return await customer_controller.delete_customer(customer_id)
