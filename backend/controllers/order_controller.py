"""
Order Controller — Full CRUD with status filter, summary, sequential IDs.
"""

import math
from datetime import datetime, timezone
from fastapi import HTTPException
from config.database import get_database
from utils.helpers import to_object_id, serialize_doc, serialize_docs
from schemas.order import OrderCreate, OrderStatusUpdate


async def list_orders(page: int, limit: int, status: str) -> dict:
    db = get_database()
    query = {}
    if status and status != "all":
        query["status"] = status

    total = await db.orders.count_documents(query)
    skip = (page - 1) * limit
    cursor = db.orders.find(query).sort("created_at", -1).skip(skip).limit(limit)
    orders = await cursor.to_list(length=limit)

    return {
        "success": True,
        "data": serialize_docs(orders),
        "total": total,
        "page": page,
        "limit": limit,
        "pages": math.ceil(total / limit) if limit else 0,
    }


async def get_order(order_id: str) -> dict:
    db = get_database()
    doc = await db.orders.find_one({"_id": to_object_id(order_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Order not found.")
    return {"success": True, "data": serialize_doc(doc)}


async def create_order(data: OrderCreate) -> dict:
    db = get_database()
    doc = data.model_dump()
    count = await db.orders.count_documents({})
    doc["order_id"] = f"#ORD-{count + 1:04d}"
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    result = await db.orders.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return {"success": True, "message": "Order created.", "data": doc}


async def update_order_status(order_id: str, data: OrderStatusUpdate) -> dict:
    db = get_database()
    result = await db.orders.update_one(
        {"_id": to_object_id(order_id)}, {"$set": {"status": data.status}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found.")
    doc = await db.orders.find_one({"_id": to_object_id(order_id)})
    return {"success": True, "message": "Order status updated.", "data": serialize_doc(doc)}


async def get_order_summary() -> dict:
    db = get_database()
    pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
    cursor = db.orders.aggregate(pipeline)
    results = await cursor.to_list(length=10)
    summary = {"pending": 0, "processing": 0, "completed": 0, "refunded": 0}
    for r in results:
        if r["_id"] in summary:
            summary[r["_id"]] = r["count"]
    return {"success": True, "data": summary}
