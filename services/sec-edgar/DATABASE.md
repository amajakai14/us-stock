# Database Setup

This document explains how to set up and manage the PostgreSQL database for the US Stock Data Collection system.

## Quick Start

### 1. Start the Database

```bash
# Start PostgreSQL database
./db.sh start

# Check status
./db.sh status
```

### 2. Set Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit if needed (defaults should work for development)
nano .env
```

### 3. Run the Application

```bash
# Backend (with database)
cd backend
source venv/bin/activate
export $(cat ../.env | xargs)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (in another terminal)
cd frontend
npm start
```

## Database Management

The `db.sh` script provides easy database management:

### Commands

```bash
./db.sh start      # Start PostgreSQL database
./db.sh stop       # Stop PostgreSQL database
./db.sh restart    # Restart PostgreSQL database
./db.sh status     # Show database status
./db.sh logs       # View database logs
./db.sh connect    # Connect with psql
./db.sh reset      # Reset database (delete all data)
./db.sh help       # Show help
```

### Examples

```bash
# Start database and wait for it to be ready
./db.sh start

# View logs
./db.sh logs

# Connect directly to database
./db.sh connect

# Check if database is running
./db.sh status

# Reset everything (start fresh)
./db.sh reset
./db.sh start
```

## Database Configuration

### Connection Details

- **Host**: localhost
- **Port**: 5432
- **Database**: us_stock_data
- **Username**: postgres
- **Password**: postgres
- **Connection URL**: `postgresql://postgres:postgres@localhost:5432/us_stock_data`
- **Async URL**: `postgresql+asyncpg://postgres:postgres@localhost:5432/us_stock_data`

### Environment Variables

Key environment variables in `.env`:

```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/us_stock_data
API_KEY=dev-api-key-12345
DEBUG=true
```

## Docker Compose Files

### `docker-compose.db.yml` - Database Only

This file contains only the PostgreSQL service and can be used independently:

```bash
docker-compose -f docker-compose.db.yml up -d
```

### `docker-compose.yml` - Full Stack

This file contains the complete application (backend, frontend, database):

```bash
docker-compose up -d
```

## Database Schema

The database schema is automatically created by SQLAlchemy when the application starts. Tables include:

- `sd_companies` - Stock discovery companies
- `sd_company_selections` - Company selection tracking
- `dc_schedules` - Data collection schedules
- `dm_exports` - Data export jobs

All tables use prefixes to indicate their domain:
- `sd_` - Stock Discovery
- `dc_` - Data Collection
- `dm_` - Data Management

## Sample Data

To populate sample data for development:

```bash
# Make sure database is running
./db.sh start

# Run the sample data script
cd backend
source venv/bin/activate
python init_sample_data.py
```

## Troubleshooting

### Database Connection Issues

1. **Check if database is running**:
   ```bash
   ./db.sh status
   ```

2. **Check database logs**:
   ```bash
   ./db.sh logs
   ```

3. **Test connection manually**:
   ```bash
   ./db.sh connect
   ```

### Port Conflicts

If port 5432 is already in use, modify `docker-compose.db.yml`:

```yaml
ports:
  - "5433:5432"  # Use port 5433 instead
```

And update the `.env` file:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/us_stock_data
```

### Reset Database

To start with a fresh database:

```bash
./db.sh reset
./db.sh start
python init_sample_data.py  # Re-populate sample data
```

## Production Considerations

For production deployment:

1. Change default passwords
2. Use environment-specific configuration
3. Set up proper backups
4. Configure connection pooling
5. Enable SSL connections
6. Set up monitoring and alerting

## Data Persistence

Database data is persisted in a Docker volume named `postgres_data`. This means:

- Data survives container restarts
- Data is preserved when you run `./db.sh stop` and `./db.sh start`
- Data is only deleted when you run `./db.sh reset`

## Backup and Restore

### Backup

```bash
# Create backup
docker-compose -f docker-compose.db.yml exec postgres pg_dump -U postgres us_stock_data > backup.sql

# Compressed backup
docker-compose -f docker-compose.db.yml exec postgres pg_dump -U postgres -Fc us_stock_data > backup.dump
```

### Restore

```bash
# Restore from SQL file
docker-compose -f docker-compose.db.yml exec -T postgres psql -U postgres us_stock_data < backup.sql

# Restore from compressed dump
docker-compose -f docker-compose.db.yml exec -T postgres pg_restore -U postgres -d us_stock_data < backup.dump
```