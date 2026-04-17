"""
Analytics schemas.
"""

from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    conversion_rate: float = 0.0
    conversion_change: float = 0.0
    avg_order_value: float = 0.0
    aov_change: float = 0.0
    bounce_rate: float = 0.0
    bounce_change: float = 0.0
    sessions: int = 0
    sessions_change: float = 0.0


class TrafficSource(BaseModel):
    source: str
    percentage: float


class DeviceBreakdown(BaseModel):
    device: str
    percentage: float
