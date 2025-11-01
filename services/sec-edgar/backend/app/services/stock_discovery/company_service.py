from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from app.infrastructure.repositories.stock_discovery import CompanyRepository
from app.shared.models.stock_discovery import (
    CompanyCreate, CompanyUpdate, CompanyResponse, CompanyListResponse,
    CompanySelectionRequest, CompanySelectionResponse, CompanySearchParams
)
from app.shared.exceptions import CompanyNotFoundError, CompanyAlreadyExistsError

class CompanyService:
    def __init__(self, db: AsyncSession):
        self.company_repo = CompanyRepository(db)

    async def create_company(self, company_data: CompanyCreate) -> CompanyResponse:
        """Create a new company"""
        # Check if company already exists
        existing = await self.company_repo.get_by_ticker(company_data.ticker_symbol)
        if existing:
            raise CompanyAlreadyExistsError(f"Company with ticker {company_data.ticker_symbol} already exists")

        # Create company
        company = await self.company_repo.create(company_data.dict())
        return CompanyResponse.from_orm(company)

    async def get_company(self, company_id: UUID) -> CompanyResponse:
        """Get company by ID"""
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with ID {company_id} not found")
        return CompanyResponse.from_orm(company)

    async def get_companies(self, params: CompanySearchParams) -> CompanyListResponse:
        """Get companies with filtering and pagination"""
        companies, total = await self.company_repo.get_all(
            page=params.page,
            size=params.size,
            query=params.query,
            exchange=params.exchange,
            sector=params.sector,
            is_selected=params.is_selected
        )

        return CompanyListResponse(
            companies=[CompanyResponse.from_orm(company) for company in companies],
            total=total,
            page=params.page,
            size=params.size
        )

    async def search_companies(self, query: str, limit: int = 10) -> List[CompanyResponse]:
        """Search companies by query"""
        companies, _ = await self.company_repo.get_all(
            page=1,
            size=limit,
            query=query
        )
        return [CompanyResponse.from_orm(company) for company in companies]

    async def get_selected_companies(self) -> List[CompanyResponse]:
        """Get all selected companies"""
        companies = await self.company_repo.get_selected_companies()
        return [CompanyResponse.from_orm(company) for company in companies]

    async def update_company(self, company_id: UUID, update_data: CompanyUpdate) -> CompanyResponse:
        """Update company information"""
        # Check if company exists
        existing = await self.company_repo.get_by_id(company_id)
        if not existing:
            raise CompanyNotFoundError(f"Company with ID {company_id} not found")

        # Update company
        update_dict = update_data.dict(exclude_unset=True)
        company = await self.company_repo.update(company_id, update_dict)

        if not company:
            raise CompanyNotFoundError(f"Company with ID {company_id} not found")

        return CompanyResponse.from_orm(company)

    async def select_company(self, company_id: UUID, selection: CompanySelectionRequest) -> CompanySelectionResponse:
        """Select or deselect a company for tracking"""
        # Check if company exists
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with ID {company_id} not found")

        # Update selection
        updated_company = await self.company_repo.select_company(
            company_id,
            selection.selected,
            selection.notes
        )

        action = "selected" if selection.selected else "deselected"
        message = f"Company {company.ticker_symbol} successfully {action}"

        return CompanySelectionResponse(
            company_id=company_id,
            selected=selection.selected,
            selection_date=updated_company.selection_date if selection.selected else None,
            message=message
        )

    async def get_available_filters(self) -> dict:
        """Get available filter options"""
        exchanges = await self.company_repo.get_unique_exchanges()
        sectors = await self.company_repo.get_unique_sectors()

        return {
            "exchanges": exchanges,
            "sectors": sectors
        }