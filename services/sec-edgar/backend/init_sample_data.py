#!/usr/bin/env python3
"""
Initialize sample data for development
"""

import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database import Base
from app.domain.stock_discovery.models import Company

# Sample companies data
SAMPLE_COMPANIES = [
    {
        "ticker_symbol": "AAPL",
        "company_name": "Apple Inc.",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "market_cap": 3000000000000.0
    },
    {
        "ticker_symbol": "MSFT",
        "company_name": "Microsoft Corporation",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "market_cap": 2800000000000.0
    },
    {
        "ticker_symbol": "GOOGL",
        "company_name": "Alphabet Inc.",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "market_cap": 1700000000000.0
    },
    {
        "ticker_symbol": "AMZN",
        "company_name": "Amazon.com Inc.",
        "exchange": "NASDAQ",
        "sector": "Consumer Discretionary",
        "market_cap": 1600000000000.0
    },
    {
        "ticker_symbol": "TSLA",
        "company_name": "Tesla Inc.",
        "exchange": "NASDAQ",
        "sector": "Consumer Discretionary",
        "market_cap": 800000000000.0
    },
    {
        "ticker_symbol": "JPM",
        "company_name": "JPMorgan Chase & Co.",
        "exchange": "NYSE",
        "sector": "Financial Services",
        "market_cap": 500000000000.0
    },
    {
        "ticker_symbol": "JNJ",
        "company_name": "Johnson & Johnson",
        "exchange": "NYSE",
        "sector": "Healthcare",
        "market_cap": 450000000000.0
    },
    {
        "ticker_symbol": "V",
        "company_name": "Visa Inc.",
        "exchange": "NYSE",
        "sector": "Financial Services",
        "market_cap": 500000000000.0
    },
    {
        "ticker_symbol": "PG",
        "company_name": "Procter & Gamble Co.",
        "exchange": "NYSE",
        "sector": "Consumer Staples",
        "market_cap": 400000000000.0
    },
    {
        "ticker_symbol": "NVDA",
        "company_name": "NVIDIA Corporation",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "market_cap": 1200000000000.0
    }
]

def init_sample_data():
    """Initialize sample data"""

    # Use synchronous connection for simple script
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/us_stock_data")

    # Replace asyncpg with psycopg2 for sync connection
    if DATABASE_URL.startswith("postgresql+asyncpg"):
        DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")

    print(f"Connecting to database: {DATABASE_URL}")

    # Create synchronous engine
    engine = create_engine(DATABASE_URL, echo=False)

    # Create tables
    print("Creating database tables...")
    Base.metadata.create_all(engine)

    # Create session
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        # Check if data already exists
        existing_count = session.query(Company).count()
        if existing_count > 0:
            print(f"Sample data already exists ({existing_count} companies). Skipping initialization.")
            return

        print("Creating sample companies...")
        for company_data in SAMPLE_COMPANIES:
            try:
                # Check if company already exists
                existing = session.query(Company).filter(
                    Company.ticker_symbol == company_data["ticker_symbol"]
                ).first()

                if not existing:
                    company = Company(**company_data)
                    session.add(company)
                    session.commit()
                    print(f"Created: {company_data['ticker_symbol']} - {company_data['company_name']}")
                else:
                    print(f"Skipped existing: {company_data['ticker_symbol']}")
            except Exception as e:
                print(f"Error creating {company_data['ticker_symbol']}: {e}")
                session.rollback()

        print("Sample data initialization completed!")

if __name__ == "__main__":
    init_sample_data()