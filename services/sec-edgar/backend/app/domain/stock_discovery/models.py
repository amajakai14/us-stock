from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import datetime
from app.infrastructure.database import Base
import uuid

class Company(Base):
    __tablename__ = "sd_companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker_symbol = Column(String(10), unique=True, nullable=False, index=True)
    company_name = Column(String(255), nullable=False)
    exchange = Column(String(50), nullable=False)
    sector = Column(String(100))
    market_cap = Column(Float)
    is_selected = Column(Boolean, default=False, nullable=False, index=True)
    selection_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Company(ticker={self.ticker_symbol}, name={self.company_name})>"

class CompanySelection(Base):
    __tablename__ = "sd_company_selections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False)
    selected_flag = Column(Boolean, nullable=False)
    selection_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(String(500))

    def __repr__(self):
        return f"<CompanySelection(company_id={self.company_id}, selected={self.selected_flag})>"