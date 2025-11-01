from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.middleware import auth_middleware
from app.api.routers import api_router
from app.infrastructure.database import init_db
import uvicorn
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="US Stock Data Collection API",
    description="API for collecting and managing US stock data from SEC Edgar",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication middleware
app.middleware("http")(auth_middleware)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Global exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with detailed logging"""
    logger.error(f"🚨 Unhandled Exception - Global Handler")
    logger.error(f"   Request Path: {request.url.path}")
    logger.error(f"   Request Method: {request.method}")
    logger.error(f"   Client IP: {request.client.host if request.client else 'unknown'}")
    logger.error(f"   Error Type: {type(exc).__name__}")
    logger.error(f"   Error Message: {str(exc)}")
    logger.error(f"   Full Stack Trace:")
    logger.error(traceback.format_exc())
    logger.error(f"   User-Agent: {request.headers.get('user-agent', 'unknown')}")
    logger.error(f"   Headers: {dict(request.headers)}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_type": type(exc).__name__,
            "error_message": str(exc)
        }
    )

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "US Stock Data Collection API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)