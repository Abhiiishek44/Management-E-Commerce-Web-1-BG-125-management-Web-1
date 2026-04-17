"""
Analytics Controller — Overview stats, traffic sources, device breakdown.
"""

from config.database import get_database


async def get_overview() -> dict:
    db = get_database()
    total_orders = await db.orders.count_documents({})
    completed = await db.orders.count_documents({"status": "completed"})

    pipeline = [
        {"$match": {"status": {"$ne": "refunded"}}},
        {"$group": {"_id": None, "total": {"$sum": "$total"}, "count": {"$sum": 1}}},
    ]
    cursor = db.orders.aggregate(pipeline)
    result = await cursor.to_list(length=1)
    total_revenue = result[0]["total"] if result else 0.0
    order_count = result[0]["count"] if result else 1

    return {
        "success": True,
        "data": {
            "conversion_rate": round((completed / total_orders * 100) if total_orders else 0, 2),
            "conversion_change": 12.0,
            "avg_order_value": round(total_revenue / order_count, 2) if order_count else 0,
            "aov_change": 8.0,
            "bounce_rate": 42.1,
            "bounce_change": -5.0,
            "sessions": 12842,
            "sessions_change": 24.0,
        },
    }


async def get_traffic() -> dict:
    return {
        "success": True,
        "data": [
            {"source": "Direct", "percentage": 65.0},
            {"source": "Social Media", "percentage": 45.0},
            {"source": "Email", "percentage": 32.0},
            {"source": "Referrals", "percentage": 18.0},
        ],
    }


async def get_devices() -> dict:
    return {
        "success": True,
        "data": [
            {"device": "Mobile", "percentage": 58.0},
            {"device": "Desktop", "percentage": 32.0},
            {"device": "Tablet", "percentage": 10.0},
        ],
    }
