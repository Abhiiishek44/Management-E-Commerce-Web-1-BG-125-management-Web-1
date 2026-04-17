"""
ForgeAdmin Backend — Database Connection
Async MongoDB client using Motor.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.settings import get_settings

settings = get_settings()

client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None


async def connect_db():
    """Initialize the MongoDB connection."""
    global client, database
    client = AsyncIOMotorClient(settings.MONGO_URL)
    database = client[settings.DB_NAME]
    # Verify connectivity
    await client.admin.command("ping")
    print(f"✅ Connected to MongoDB: {settings.DB_NAME}")


async def close_db():
    """Close the MongoDB connection."""
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed.")


def get_database() -> AsyncIOMotorDatabase:
    """Return the database instance."""
    return database
