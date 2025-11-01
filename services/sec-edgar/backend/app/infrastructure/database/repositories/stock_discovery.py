from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from app.domain.stock_discovery.models import Company, CompanySelection

class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, company_data: dict) -> Company:
        """Create a new company"""
        company = Company(**company_data)
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def get_by_id(self, company_id: UUID) -> Optional[Company]:
        """Get company by ID"""
        result = await self.db.execute(
            select(Company).where(Company.id == company_id)
        )
        return result.scalar_one_or_none()

    async def get_by_ticker(self, ticker_symbol: str) -> Optional[Company]:
        """Get company by ticker symbol"""
        result = await self.db.execute(
            select(Company).where(Company.ticker_symbol == ticker_symbol.upper())
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        size: int = 50,
        query: Optional[str] = None,
        exchange: Optional[str] = None,
        sector: Optional[str] = None,
        is_selected: Optional[bool] = None
    ) -> Tuple[List[Company], int]:
        """Get companies with filtering and pagination"""

        # Build base query
        filters = []

        if query:
            filters.append(
                or_(
                    Company.ticker_symbol.ilike(f"%{query}%"),
                    Company.company_name.ilike(f"%{query}%")
                )
            )

        if exchange:
            filters.append(Company.exchange == exchange)

        if sector:
            filters.append(Company.sector == sector)

        if is_selected is not None:
            filters.append(Company.is_selected == is_selected)

        # Count query
        count_query = select(func.count(Company.id))
        if filters:
            count_query = count_query.where(and_(*filters))

        count_result = await self.db.execute(count_query)
        total = count_result.scalar()

        # Data query with pagination
        data_query = select(Company)
        if filters:
            data_query = data_query.where(and_(*filters))

        data_query = data_query.offset((page - 1) * size).limit(size)
        data_query = data_query.order_by(Company.ticker_symbol)

        result = await self.db.execute(data_query)
        companies = result.scalars().all()

        return companies, total

    async def get_selected_companies(self) -> List[Company]:
        """Get all selected companies"""
        result = await self.db.execute(
            select(Company)
            .where(Company.is_selected == True)
            .order_by(Company.ticker_symbol)
        )
        return result.scalars().all()

    async def update(self, company_id: UUID, update_data: dict) -> Optional[Company]:
        """Update company"""
        update_data["updated_at"] = datetime.utcnow()

        result = await self.db.execute(
            update(Company)
            .where(Company.id == company_id)
            .values(**update_data)
            .returning(Company)
        )

        await self.db.commit()
        return result.scalar_one_or_none()

    async def select_company(self, company_id: UUID, selected: bool, notes: Optional[str] = None) -> Optional[Company]:
        """Select or deselect a company for tracking"""
        update_data = {
            "is_selected": selected,
            "updated_at": datetime.utcnow()
        }

        if selected:
            update_data["selection_date"] = datetime.utcnow()

        result = await self.db.execute(
            update(Company)
            .where(Company.id == company_id)
            .values(**update_data)
            .returning(Company)
        )

        await self.db.commit()
        return result.scalar_one_or_none()

    async def get_unique_exchanges(self) -> List[str]:
        """Get list of unique exchanges"""
        result = await self.db.execute(
            select(Company.exchange).distinct().order_by(Company.exchange)
        )
        return [row[0] for row in result]

    async def get_unique_sectors(self) -> List[str]:
        """Get list of unique sectors"""
        result = await self.db.execute(
            select(Company.sector)
            .where(Company.sector.isnot(None))
            .distinct()
            .order_by(Company.sector)
        )
        return [row[0] for row in result]