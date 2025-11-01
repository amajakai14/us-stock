from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_schedules():
    """Get collection schedules - TODO: Implement"""
    return {"message": "Data collection schedules - Coming soon"}

@router.post("/")
async def create_schedule():
    """Create collection schedule - TODO: Implement"""
    return {"message": "Create schedule - Coming soon"}