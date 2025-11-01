from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import os
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("API_KEY", "dev-api-key-12345")

async def auth_middleware(request: Request, call_next):
    """Simple API key authentication middleware with enhanced logging"""

    # Skip authentication for health check and docs
    if request.url.path in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
        response = await call_next(request)
        return response

    # Check API key in header
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        # Log 401 error with details
        logger.error(f"❌ 401 Unauthorized - API Key Authentication Failed")
        logger.error(f"   Request Path: {request.url.path}")
        logger.error(f"   Request Method: {request.method}")
        logger.error(f"   Client IP: {request.client.host if request.client else 'unknown'}")
        logger.error(f"   API Key Provided: {'Yes' if api_key else 'No'}")
        logger.error(f"   API Key Valid: {api_key == API_KEY if api_key else 'N/A'}")
        logger.error(f"   Expected API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
        if api_key:
            logger.error(f"   Received API Key: {api_key[:8]}...{api_key[-4:]}")
        logger.error(f"   User-Agent: {request.headers.get('user-agent', 'unknown')}")

        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or missing API key"}
        )

    try:
        response = await call_next(request)
        return response
    except Exception as e:
        # Log 500 error with full stack trace
        logger.error(f"💥 500 Internal Server Error")
        logger.error(f"   Request Path: {request.url.path}")
        logger.error(f"   Request Method: {request.method}")
        logger.error(f"   Client IP: {request.client.host if request.client else 'unknown'}")
        logger.error(f"   Error Type: {type(e).__name__}")
        logger.error(f"   Error Message: {str(e)}")
        logger.error(f"   Full Stack Trace:")
        logger.error(traceback.format_exc())
        logger.error(f"   User-Agent: {request.headers.get('user-agent', 'unknown')}")

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error_type": type(e).__name__}
        )