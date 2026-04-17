"""
Settings Controller — Get and update store settings.
"""

from config.database import get_database
from schemas.settings import SettingsUpdate

_DEFAULT_SETTINGS = {
    "store_name": "BackForge Store",
    "store_email": "admin@forgecart.com",
    "currency": "USD",
    "timezone": "UTC",
    "language": "en",
    "notifications_enabled": True,
    "maintenance_mode": False,
}


async def get_settings() -> dict:
    db = get_database()
    doc = await db.settings.find_one({"_type": "store_settings"})
    if not doc:
        doc = {**_DEFAULT_SETTINGS, "_type": "store_settings"}
        await db.settings.insert_one(doc)
        doc = await db.settings.find_one({"_type": "store_settings"})
    doc.pop("_id", None)
    doc.pop("_type", None)
    return {"success": True, "data": doc}


async def update_settings(data: SettingsUpdate) -> dict:
    db = get_database()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        return await get_settings()
    await db.settings.update_one(
        {"_type": "store_settings"},
        {"$set": update_data},
        upsert=True,
    )
    return await get_settings()
