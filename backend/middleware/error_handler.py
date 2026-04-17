"""
ForgeAdmin Backend — Global Error Handler Middleware
Catches unhandled exceptions and returns structured JSON responses.
"""

import logging
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger("forgeadmin")


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(
                "Unhandled error on %s %s: %s\n%s",
                request.method,
                request.url.path,
                str(exc),
                traceback.format_exc(),
            )
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal server error.",
                    "detail": str(exc) if logger.isEnabledFor(logging.DEBUG) else None,
                },
            )
