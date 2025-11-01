#!/usr/bin/env python3
"""
Migrate NASDAQ screener data to database
Filters for US companies and maps to Company entity design
"""

import os
import sys
import csv
import re
from typing import List, Dict, Optional
from decimal import Decimal, InvalidOperation
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.stock_discovery.models import Company
from app.infrastructure.database import Base

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/us_stock_data")

def parse_market_cap(market_cap_str: str) -> Optional[float]:
    """Parse market cap string to float, handling various formats"""
    if not market_cap_str or market_cap_str.strip() == '' or market_cap_str == '0.00':
        return None

    try:
        # Remove commas and dollar signs, convert to float
        clean_str = market_cap_str.replace(',', '').replace('$', '').strip()
        return float(clean_str)
    except (ValueError, InvalidOperation):
        return None

def clean_company_name(name: str) -> str:
    """Clean company name by removing common suffixes"""
    if not name:
        return ""

    # Remove common stock suffixes
    suffixes = [
        " Common Stock", " Class A Common Stock", " Class B Common Stock",
        " Ordinary Shares", " American Depositary Shares", " Depositary Shares",
        " Units", " Rights", " Warrants", " Class A Ordinary Shares",
        " Class B Ordinary Shares", " Inc.", " Corporation", " Corp.",
        " Limited", " Ltd.", " LLC", " PLC"
    ]

    cleaned_name = name.strip()
    for suffix in suffixes:
        if cleaned_name.endswith(suffix):
            cleaned_name = cleaned_name[:-len(suffix)].strip()

    return cleaned_name

def is_us_company(country: str) -> bool:
    """Check if company is from United States"""
    if not country:
        return False

    us_variants = [
        "United States", "USA", "US", "U.S.", "U.S.A.", "United States of America"
    ]

    return country.strip() in us_variants

def clean_sector(sector: str) -> Optional[str]:
    """Clean and standardize sector name"""
    if not sector or sector.strip() == '':
        return None

    # Map various sector names to standard ones
    sector_mapping = {
        "Technology": "Technology",
        "Industrials": "Industrials",
        "Finance": "Financial Services",
        "Health Care": "Healthcare",
        "Consumer Discretionary": "Consumer Discretionary",
        "Consumer Staples": "Consumer Staples",
        "Real Estate": "Real Estate",
        "Energy": "Energy",
        "Utilities": "Utilities",
        "Basic Materials": "Basic Materials",
        "Communication Services": "Communication Services"
    }

    cleaned_sector = sector.strip()
    return sector_mapping.get(cleaned_sector, cleaned_sector)

def read_csv_data(file_path: str) -> List[Dict]:
    """Read and parse CSV data"""
    companies = []

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Filter for US companies only
            if not is_us_company(row.get('Country', '')):
                continue

            # Extract and clean data
            symbol = row.get('Symbol', '').strip()
            name = clean_company_name(row.get('Name', ''))
            last_sale = row.get('Last Sale', '')
            market_cap_str = row.get('Market Cap', '')
            sector = clean_sector(row.get('Sector', ''))
            country = row.get('Country', '').strip()

            # Skip rows with missing essential data
            if not symbol or not name:
                continue

            # Skip obvious non-stock entries (warrants, rights, etc.)
            skip_patterns = [
                r'.*Rights$', r'.*Warrants?$', r'.*Units$', r'.*Notes?$',
                r'.*Bond$', r'.*Preferred$', r'.*Series \w+'
            ]

            if any(re.match(pattern, name, re.IGNORECASE) for pattern in skip_patterns):
                continue

            market_cap = parse_market_cap(market_cap_str)

            companies.append({
                'ticker_symbol': symbol,
                'company_name': name,
                'exchange': 'NASDAQ',  # All from NASDAQ screener
                'sector': sector,
                'market_cap': market_cap,
                'country': country
            })

    return companies

def migrate_companies(companies: List[Dict], session) -> Dict:
    """Migrate companies to database with conflict handling"""
    stats = {
        'total': len(companies),
        'new': 0,
        'updated': 0,
        'skipped': 0,
        'errors': []
    }

    for company_data in companies:
        try:
            # Check if company already exists
            existing = session.query(Company).filter(
                Company.ticker_symbol == company_data['ticker_symbol']
            ).first()

            if existing:
                # Update existing company if needed
                updated = False

                if existing.company_name != company_data['company_name']:
                    existing.company_name = company_data['company_name']
                    updated = True

                if existing.sector != company_data['sector']:
                    existing.sector = company_data['sector']
                    updated = True

                if existing.market_cap != company_data['market_cap']:
                    existing.market_cap = company_data['market_cap']
                    updated = True

                if updated:
                    existing.updated_at = datetime.utcnow()
                    stats['updated'] += 1
                else:
                    stats['skipped'] += 1
            else:
                # Create new company
                new_company = Company(
                    ticker_symbol=company_data['ticker_symbol'],
                    company_name=company_data['company_name'],
                    exchange=company_data['exchange'],
                    sector=company_data['sector'],
                    market_cap=company_data['market_cap']
                )
                session.add(new_company)
                stats['new'] += 1

        except Exception as e:
            stats['errors'].append(f"Error processing {company_data['ticker_symbol']}: {str(e)}")
            print(f"❌ Error processing {company_data['ticker_symbol']}: {e}")

    return stats

def main():
    """Main migration function"""
    import argparse

    parser = argparse.ArgumentParser(description='Migrate NASDAQ data to database')
    parser.add_argument('--force', action='store_true', help='Skip confirmation prompt')
    args = parser.parse_args()

    print("🚀 Starting NASDAQ data migration...")

    # File path
    csv_file = "../assets/nasdaq_screener_1761999846975.csv"

    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return

    try:
        # Create database connection
        print(f"📊 Connecting to database: {DATABASE_URL}")
        engine = create_engine(DATABASE_URL, echo=False)
        SessionLocal = sessionmaker(bind=engine)

        # Create tables if they don't exist
        print("🔧 Ensuring database tables exist...")
        Base.metadata.create_all(engine)

        # Read CSV data
        print(f"📖 Reading CSV file: {csv_file}")
        companies = read_csv_data(csv_file)

        print(f"📋 Found {len(companies)} US companies in CSV")

        if not companies:
            print("⚠️  No US companies found in CSV file")
            return

        # Show sample data
        print("\n📝 Sample companies:")
        for i, company in enumerate(companies[:5]):
            print(f"  {i+1}. {company['ticker_symbol']} - {company['company_name']} "
                  f"({company['sector'] or 'No sector'}) - ${company['market_cap'] or 'N/A'}")

        if len(companies) > 5:
            print(f"  ... and {len(companies) - 5} more")

        # Confirm migration
        if not args.force:
            response = input(f"\nProceed with migrating {len(companies)} companies? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("❌ Migration cancelled")
                return
        else:
            print(f"\n🚀 Force mode: Proceeding with migration of {len(companies)} companies...")

        # Migrate data
        with SessionLocal() as session:
            stats = migrate_companies(companies, session)

            # Commit changes
            session.commit()

            # Show results
            print("\n✅ Migration completed!")
            print(f"   Total companies processed: {stats['total']}")
            print(f"   New companies added: {stats['new']}")
            print(f"   Existing companies updated: {stats['updated']}")
            print(f"   Companies skipped (no changes): {stats['skipped']}")

            if stats['errors']:
                print(f"   Errors encountered: {len(stats['errors'])}")
                for error in stats['errors'][:5]:  # Show first 5 errors
                    print(f"     - {error}")
                if len(stats['errors']) > 5:
                    print(f"     ... and {len(stats['errors']) - 5} more errors")

            # Verify counts
            total_companies = session.query(Company).count()
            us_companies = session.query(Company).filter(Company.exchange == 'NASDAQ').count()

            print(f"\n📊 Database Statistics:")
            print(f"   Total companies in database: {total_companies}")
            print(f"   NASDAQ companies: {us_companies}")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n🎉 NASDAQ data migration completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())