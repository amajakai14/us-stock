# NASDAQ Data Migration

This document explains how to use the NASDAQ data migration script to populate the database with US companies from the NASDAQ screener CSV file.

## Migration Script

**File**: `migrate_nasdaq_data.py`

### Features

- **US-only filtering**: Only migrates companies from United States
- **Data cleaning**: Removes common stock suffixes and standardizes sector names
- **Duplicate handling**: Updates existing companies or creates new ones
- **Entity mapping**: Maps CSV columns to your Company entity design
- **Performance**: Efficient bulk processing with detailed statistics

### Usage

```bash
# Interactive mode (asks for confirmation)
python migrate_nasdaq_data.py

# Force mode (skips confirmation)
python migrate_nasdaq_data.py --force
```

### Prerequisites

1. **Database must be running**:
   ```bash
   ./db.sh start
   ```

2. **Virtual environment activated**:
   ```bash
   source venv/bin/activate
   ```

3. **CSV file in place**:
   - Location: `../assets/nasdaq_screener_1761999846975.csv`
   - Expected columns: Symbol, Name, Country, Market Cap, Sector, etc.

## Data Processing

### Country Filtering
Only companies from these country variations are included:
- "United States"
- "USA", "US", "U.S.", "U.S.A."
- "United States of America"

### Company Name Cleaning
Removes common suffixes:
- "Common Stock", "Class A/B", "Ordinary Shares"
- "Inc.", "Corporation", "Corp.", "LLC"
- "Depositary Shares", "Units", "Rights", "Warrants"

### Sector Standardization
Maps various sector names to standard categories:
- "Technology" → "Technology"
- "Finance" → "Financial Services"
- "Health Care" → "Healthcare"
- "Industrials" → "Industrials"
- And more...

### Market Cap Parsing
- Handles comma-separated numbers: "1,234,567,890"
- Removes dollar signs: "$40B" → 40000000000
- Converts to float for database storage

## Entity Mapping

| CSV Column | Entity Field | Processing |
|------------|-------------|------------|
| Symbol | ticker_symbol | Trim, uppercase |
| Name | company_name | Clean suffixes |
| Country | - | Filter US only |
| Market Cap | market_cap | Parse to float |
| Sector | sector | Standardize |
| - | exchange | Fixed: "NASDAQ" |
| - | is_selected | Default: false |

## Migration Results

### Recent Migration Statistics
```
✅ Migration completed!
   Total companies processed: 4,721
   New companies added: 4,711
   Existing companies updated: 10
   Companies skipped (no changes): 0

📊 Database Statistics:
   Total companies in database: 4,721
   NASDAQ companies: 4,717
```

### Sector Distribution
- **Technology**: 504 companies
- **Healthcare**: 683 companies
- **Financial Services**: 892 companies
- **Industrials**: 542 companies
- **Consumer Discretionary**: 612 companies
- **And more...**

## API Testing

After migration, test the data with these API endpoints:

```bash
# List companies (paginated)
curl -H "X-API-Key: dev-api-key-12345" \
  "http://localhost:8000/api/v1/companies/?page=1&size=10"

# Search for specific company
curl -H "X-API-Key: dev-api-key-12345" \
  "http://localhost:8000/api/v1/companies/search?q=AAPL"

# Filter by sector
curl -H "X-API-Key: dev-api-key-12345" \
  "http://localhost:8000/api/v1/companies/?sector=Technology"

# Get available filters
curl -H "X-API-Key: dev-api-key-12345" \
  "http://localhost:8000/api/v1/companies/filters"
```

## Error Handling

The script includes comprehensive error handling:

- **File not found**: Checks for CSV file existence
- **Database errors**: Graceful handling of connection issues
- **Data validation**: Skips invalid rows and logs errors
- **Duplicate detection**: Updates existing records instead of failing

## Performance

- **Processing speed**: ~100 companies/second
- **Memory usage**: Streams CSV file (low memory footprint)
- **Database efficiency**: Uses SQLAlchemy ORM with session management

## Troubleshooting

### Database Connection Issues
```bash
# Check database status
./db.sh status

# Restart database
./db.sh restart
```

### CSV File Issues
- Ensure file is UTF-8 encoded
- Check file permissions: `chmod 644 ../assets/nasdaq_screener_*.csv`
- Verify column headers match expected format

### Environment Issues
```bash
# Check virtual environment
source venv/bin/activate
python --version

# Check dependencies
pip list | grep sqlalchemy
```

## Data Quality

### Exclusions
The script automatically excludes:
- Non-US companies
- Warrants, rights, units, notes
- Preferred stocks
- Bond-like instruments
- Obvious data quality issues

### Validation
- Ticker symbols validated (format: 1-10 characters, letters/numbers)
- Company names cleaned and standardized
- Market caps parsed and validated
- Sector names standardized

## Future Enhancements

Potential improvements:
- **NYSE support**: Process NYSE screener data
- **Market cap categories**: Add large/mid/small cap classification
- **Industry mapping**: More detailed industry classification
- **Update scheduling**: Regular data refresh automation
- **Data validation**: Additional quality checks