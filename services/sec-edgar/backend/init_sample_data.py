#!/usr/bin/env python3
"""
Initialize sample data for development
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import AsyncSessionLocal, init_db
from app.infrastructure.database.repositories.stock_discovery import CompanyRepository

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

async def init_sample_data():
    """Initialize sample data"""
    print("Initializing database...")
    await init_db()

    async with AsyncSessionLocal() as db:
        company_repo = CompanyRepository(db)

        # Check if data already exists
        existing_count = await company_repo.get_all(page=1, size=1)
        if existing_count[1] > 0:
            print("Sample data already exists. Skipping initialization.")
            return

        print("Creating sample companies...")
        for company_data in SAMPLE_COMPANIES:
            try:
                # Check if company already exists
                existing = await company_repo.get_by_ticker(company_data["ticker_symbol"])
                if not existing:
                    await company_repo.create(company_data)
                    print(f"Created: {company_data['ticker_symbol']} - {company_data['company_name']}")
                else:
                    print(f"Skipped existing: {company_data['ticker_symbol']}")
            except Exception as e:
                print(f"Error creating {company_data['ticker_symbol']}: {e}")

        print("Sample data initialization completed!")

if __name__ == "__main__":
    asyncio.run(init_sample_data())