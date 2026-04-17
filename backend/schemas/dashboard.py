"""
Dashboard schemas.
"""

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_revenue: float = 0.0
    revenue_change: float = 0.0
    total_orders: int = 0
    orders_change: float = 0.0
    total_customers: int = 0
    customers_change: float = 0.0
    total_products: int = 0
    products_change: float = 0.0


class SalesByCategory(BaseModel):
    name: str
    percentage: float
