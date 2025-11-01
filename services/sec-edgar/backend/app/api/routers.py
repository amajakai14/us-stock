from fastapi import APIRouter
from .routers import stock_discovery, data_collection, data_management

api_router = APIRouter()

# Include routers for each bounded context
api_router.include_router(
    stock_discovery.router,
    prefix="/companies",
    tags=["Stock Discovery"]
)

api_router.include_router(
    data_collection.router,
    prefix="/schedules",
    tags=["Data Collection"]
)

api_router.include_router(
    data_management.router,
    prefix="/data",
    tags=["Data Management"]
)