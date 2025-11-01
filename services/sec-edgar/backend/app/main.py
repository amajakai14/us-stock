from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.middleware import auth_middleware
from app.api.routers import api_router
from app.infrastructure.database import init_db
import uvicorn

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