"""
ForgeAdmin Backend — Main Application Entry Point
FastAPI app with middleware, routes, and MongoDB lifecycle.
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import connect_db, close_db
from middleware.logging import LoggingMiddleware
from middleware.error_handler import ErrorHandlerMiddleware

# --- Route imports ---
from routes.auth import router as auth_router
from routes.products import router as products_router
from routes.categories import router as categories_router
from routes.orders import router as orders_router
from routes.customers import router as customers_router
from routes.reviews import router as reviews_router
from routes.promotions import router as promotions_router
from routes.staff import router as staff_router
from routes.dashboard import router as dashboard_router
from routes.analytics import router as analytics_router
from routes.settings import router as settings_router

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("forgeadmin")


# ---------------------------------------------------------------------------
# App lifecycle — connect / disconnect MongoDB
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    logger.info("🚀 ForgeAdmin API is ready.")
    yield
    await close_db()


# ---------------------------------------------------------------------------
# Create FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="ForgeAdmin API",
    description="Backend API for the ForgeAdmin E-Commerce Dashboard",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware (order matters — outermost first)
# ---------------------------------------------------------------------------
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://0.0.0.0:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Register all routers
# ---------------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(analytics_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(customers_router)
app.include_router(reviews_router)
app.include_router(promotions_router)
app.include_router(staff_router)
app.include_router(settings_router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "app": "ForgeAdmin API", "version": "1.0.0"}
