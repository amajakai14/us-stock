from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.infrastructure.database import get_db
from app.services.stock_discovery.company_service import CompanyService
from app.shared.models.stock_discovery import (
    CompanyCreate, CompanyUpdate, CompanyResponse, CompanyListResponse,
    CompanySelectionRequest, CompanySelectionResponse, CompanySearchParams
)

router = APIRouter()

def get_company_service(db: AsyncSession = Depends(get_db)) -> CompanyService:
    return CompanyService(db)

@router.get("/", response_model=CompanyListResponse)
async def get_companies(
    query: str = Query(None, description="Search query for ticker or company name"),
    exchange: str = Query(None, description="Filter by exchange"),
    sector: str = Query(None, description="Filter by sector"),
    is_selected: bool = Query(None, description="Filter by selection status"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    company_service: CompanyService = Depends(get_company_service)
):
    """Get list of companies with filtering and pagination"""
    params = CompanySearchParams(
        query=query,
        exchange=exchange,
        sector=sector,
        is_selected=is_selected,
        page=page,
        size=size
    )
    return await company_service.get_companies(params)

@router.get("/search", response_model=List[CompanyResponse])
async def search_companies(
    q: str = Query(..., min_length=1, max_length=50, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    company_service: CompanyService = Depends(get_company_service)
):
    """Search companies by ticker symbol or company name"""
    return await company_service.search_companies(q, limit)

@router.get("/selected", response_model=List[CompanyResponse])
async def get_selected_companies(
    company_service: CompanyService = Depends(get_company_service)
):
    """Get all companies selected for data collection"""
    return await company_service.get_selected_companies()

@router.get("/filters")
async def get_available_filters(
    company_service: CompanyService = Depends(get_company_service)
):
    """Get available filter options (exchanges, sectors)"""
    return await company_service.get_available_filters()

@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: str,
    company_service: CompanyService = Depends(get_company_service)
):
    """Get company by ID"""
    try:
        from uuid import UUID
        company_uuid = UUID(company_id)
        return await company_service.get_company(company_uuid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid company ID format")

@router.post("/", response_model=CompanyResponse)
async def create_company(
    company_data: CompanyCreate,
    company_service: CompanyService = Depends(get_company_service)
):
    """Create a new company"""
    return await company_service.create_company(company_data)

@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: str,
    update_data: CompanyUpdate,
    company_service: CompanyService = Depends(get_company_service)
):
    """Update company information"""
    try:
        from uuid import UUID
        company_uuid = UUID(company_id)
        return await company_service.update_company(company_uuid, update_data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid company ID format")

@router.post("/{company_id}/select", response_model=CompanySelectionResponse)
async def select_company(
    company_id: str,
    selection: CompanySelectionRequest,
    company_service: CompanyService = Depends(get_company_service)
):
    """Select or deselect a company for data collection"""
    try:
        from uuid import UUID
        company_uuid = UUID(company_id)
        return await company_service.select_company(company_uuid, selection)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid company ID format")