from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class CompanyBase(BaseModel):
    ticker_symbol: str = Field(..., min_length=1, max_length=10, pattern="^[A-Z]+$")
    company_name: str = Field(..., min_length=1, max_length=255)
    exchange: str = Field(..., min_length=1, max_length=50)
    sector: Optional[str] = Field(None, max_length=100)
    market_cap: Optional[float] = Field(None, ge=0)

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    exchange: Optional[str] = Field(None, min_length=1, max_length=50)
    sector: Optional[str] = Field(None, max_length=100)
    market_cap: Optional[float] = Field(None, ge=0)

class CompanyResponse(CompanyBase):
    id: UUID
    is_selected: bool
    selection_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        populate_by_name = True

class CompanyListResponse(BaseModel):
    companies: List[CompanyResponse]
    total: int
    page: int
    size: int

class CompanySelectionRequest(BaseModel):
    selected: bool
    notes: Optional[str] = Field(None, max_length=500)

class CompanySelectionResponse(BaseModel):
    company_id: UUID
    selected: bool
    selection_date: datetime
    message: str

class CompanySearchParams(BaseModel):
    query: Optional[str] = Field(None, min_length=1, max_length=50)
    exchange: Optional[str] = None
    sector: Optional[str] = None
    is_selected: Optional[bool] = None
    page: int = Field(1, ge=1)
    size: int = Field(50, ge=1, le=100)