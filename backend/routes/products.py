"""
Product Routes — /api/products
"""

from fastapi import APIRouter, Depends, Query
from controllers import product_controller
from schemas.product import ProductCreate, ProductUpdate
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("")
async def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(""),
    _user: dict = Depends(get_current_user),
):
    return await product_controller.list_products(page, limit, search)


@router.get("/{product_id}")
async def get_product(product_id: str, _user: dict = Depends(get_current_user)):
    return await product_controller.get_product(product_id)


@router.post("")
async def create_product(data: ProductCreate, _user: dict = Depends(get_current_user)):
    return await product_controller.create_product(data)


@router.put("/{product_id}")
async def update_product(
    product_id: str, data: ProductUpdate, _user: dict = Depends(get_current_user)
):
    return await product_controller.update_product(product_id, data)


@router.delete("/{product_id}")
async def delete_product(product_id: str, _user: dict = Depends(get_current_user)):
    return await product_controller.delete_product(product_id)
