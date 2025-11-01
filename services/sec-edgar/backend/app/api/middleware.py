from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import os

API_KEY = os.getenv("API_KEY", "dev-api-key-12345")

async def auth_middleware(request: Request, call_next):
    """Simple API key authentication middleware"""

    # Skip authentication for health check and docs
    if request.url.path in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
        response = await call_next(request)
        return response

    # Check API key in header
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or missing API key"}
        )

    response = await call_next(request)
    return response