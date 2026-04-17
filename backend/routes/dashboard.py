"""
Dashboard Routes — /api/dashboard
"""

from fastapi import APIRouter, Depends
from controllers import dashboard_controller
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def get_stats(_user: dict = Depends(get_current_user)):
    return await dashboard_controller.get_stats()


@router.get("/sales-by-category")
async def get_sales_by_category(_user: dict = Depends(get_current_user)):
    return await dashboard_controller.get_sales_by_category()
