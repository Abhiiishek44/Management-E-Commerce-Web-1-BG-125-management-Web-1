"""
Dashboard Controller — Aggregated stats and sales-by-category.
"""

from datetime import datetime, timezone

from config.database import get_database


async def get_stats() -> dict:
    db = get_database()

    total_products = await db.products.count_documents({})
    total_customers = await db.customers.count_documents({})
    total_orders = await db.orders.count_documents({})

    # Aggregate total revenue from non-refunded orders
    pipeline = [
        {"$match": {"status": {"$ne": "refunded"}}},
        {"$group": {"_id": None, "total": {"$sum": "$total"}}},
    ]
    cursor = db.orders.aggregate(pipeline)
    result = await cursor.to_list(length=1)
    total_revenue = result[0]["total"] if result else 0.0

    return {
        "success": True,
        "data": {
            "total_revenue": total_revenue,
            "revenue_change": 12.5,
            "total_orders": total_orders,
            "orders_change": 8.2,
            "total_customers": total_customers,
            "customers_change": 5.1,
            "total_products": total_products,
            "products_change": -2.3,
        },
    }


async def get_sales_by_category() -> dict:
    db = get_database()
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    cursor = db.products.aggregate(pipeline)
    results = await cursor.to_list(length=20)
    total = sum(r["count"] for r in results) or 1
    data = [
        {"name": r["_id"] or "Uncategorized", "percentage": round(r["count"] / total * 100, 1)}
        for r in results
    ]
    return {"success": True, "data": data}


async def get_revenue_overview() -> dict:
    db = get_database()

    pipeline = [
        {
            "$addFields": {
                "created_at_date": {
                    "$cond": [
                        {"$eq": [{"$type": "$created_at"}, "date"]},
                        "$created_at",
                        {
                            "$dateFromString": {
                                "dateString": "$created_at",
                                "onError": None,
                                "onNull": None,
                            }
                        },
                    ]
                }
            }
        },
        {
            "$match": {
                "status": {"$ne": "refunded"},
                "created_at_date": {"$ne": None},
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at_date"},
                    "month": {"$month": "$created_at_date"},
                },
                "revenue": {"$sum": "$total"},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]

    cursor = db.orders.aggregate(pipeline)
    results = await cursor.to_list(length=120)

    revenue_map = {
        f"{r['_id']['year']:04d}-{r['_id']['month']:02d}": round(float(r.get("revenue", 0)), 2)
        for r in results
    }

    now = datetime.now(timezone.utc)
    months = []
    for i in range(5, -1, -1):
        month_index = now.year * 12 + (now.month - 1) - i
        year = month_index // 12
        month = (month_index % 12) + 1
        key = f"{year:04d}-{month:02d}"
        label = datetime(year, month, 1).strftime("%b")
        months.append(
            {
                "month": label,
                "key": key,
                "revenue": revenue_map.get(key, 0.0),
            }
        )

    return {"success": True, "data": months}
