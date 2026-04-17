"""
Settings schemas.
"""

from pydantic import BaseModel
from typing import Optional


class StoreSettings(BaseModel):
    store_name: str = "BackForge Store"
    store_email: str = "admin@forgecart.com"
    currency: str = "USD"
    timezone: str = "UTC"
    language: str = "en"
    notifications_enabled: bool = True
    maintenance_mode: bool = False


class SettingsUpdate(BaseModel):
    store_name: Optional[str] = None
    store_email: Optional[str] = None
    currency: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    maintenance_mode: Optional[bool] = None
