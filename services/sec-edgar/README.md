# US Stock Data Collection System

A comprehensive system for discovering US stock tickers and collecting SEC Edgar data with automated scheduling capabilities.

## 🎯 Features

### MVP Features (Implemented)
- **Stock Discovery**: Browse and search all active US stock tickers
- **Company Selection**: Select/deselect companies for data collection tracking
- **Data Collection Scheduling**: Configure automated SEC Edgar data collection (backend ready)

### Future Features (Planned)
- **Financial Report Date Tracking**: Monitor upcoming SEC filing deadlines
- **Time-Series Data Visualization**: View historical data with charts
- **Data Export**: Export collected data in various formats (CSV, JSON, Excel)

## 🏗️ Architecture

- **Backend**: Python + FastAPI with SQLAlchemy ORM
- **Frontend**: React + TypeScript with Material-UI
- **Database**: PostgreSQL with Docker containerization
- **API**: RESTful design with OpenAPI documentation
- **Domain Design**: Domain-Driven Design (DDD) with bounded contexts

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Development Setup

1. **Clone and navigate to project**:
   ```bash
   git clone <repository-url>
   cd us-stock/services/sec-edgar
   ```

2. **Start all services**:
   ```bash
   docker-compose up -d
   ```

3. **Initialize sample data** (one-time setup):
   ```bash
   docker-compose exec backend python init_sample_data.py
   ```

4. **Access the applications**:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### Development Workflow

#### Backend Development
```bash
# Enter backend container
docker-compose exec backend bash

# Install new dependencies
pip install package-name

# Run tests
pytest

# Create database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

#### Frontend Development
```bash
# Frontend hot-reloads automatically when files change
# Check logs with: docker-compose logs -f frontend
```

## 📁 Project Structure

```
project-root/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes by bounded context
│   │   ├── services/          # Application service layer
│   │   ├── domain/            # Rich domain models
│   │   ├── infrastructure/   # Database, external APIs
│   │   └── shared/           # Common utilities
│   ├── migrations/           # Database migrations
│   └── tests/               # Backend tests
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Complete page implementations
│   │   ├── services/        # API client code
│   │   └── utils/           # Frontend utilities
│   └── public/
├── .aidlc/                    # AI-DLC workflow artifacts
├── docker-compose.yml         # Development environment
└── README.md                 # This file
```

## 🔧 Bounded Contexts

### Stock Discovery
- **Purpose**: Company discovery and selection management
- **Entities**: Company, CompanySelection
- **API Endpoints**: `/api/v1/companies/*`

### Data Collection
- **Purpose**: SEC Edgar data collection and scheduling
- **Entities**: CollectionSchedule, SECData, FinancialReportDates
- **API Endpoints**: `/api/v1/schedules/*` (Coming soon)

### Data Management
- **Purpose**: Data viewing, export, and historical management
- **Entities**: TimeSeriesData, DataExport
- **API Endpoints**: `/api/v1/data/*` (Coming soon)

## 🔌 API Usage

### Authentication
All API endpoints require an API key passed in the `X-API-Key` header:
```
X-API-Key: dev-api-key-12345
```

### Example API Calls

#### Get Companies
```bash
curl -H "X-API-Key: dev-api-key-12345" \
     http://localhost:8000/api/v1/companies
```

#### Search Companies
```bash
curl -H "X-API-Key: dev-api-key-12345" \
     "http://localhost:8000/api/v1/companies/search?q=AAPL"
```

#### Select Company
```bash
curl -X POST \
     -H "X-API-Key: dev-api-key-12345" \
     -H "Content-Type: application/json" \
     -d '{"selected": true}' \
     http://localhost:8000/api/v1/companies/{company_id}/select
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app

# Run specific test file
docker-compose exec backend pytest tests/test_companies.py
```

### Frontend Tests
```bash
# Run tests
docker-compose exec frontend npm test

# Run tests in watch mode
docker-compose exec frontend npm test --watch
```

## 📊 Database Schema

### Tables
- `sd_companies`: Company information with selection status
- `sd_company_selections`: Company selection tracking
- `dc_schedules`: Data collection schedules (Coming soon)
- `dc_sec_data`: SEC Edgar filing data (Coming soon)
- `dm_exports`: Data export tracking (Coming soon)
- `dm_time_series`: Time-series data (Coming soon)

### Database Connection
```bash
# Connect to database
docker-compose exec postgres psql -U postgres -d us_stock_data

# View tables
\dt

# View sample data
SELECT * FROM sd_companies LIMIT 5;
```

## 🔐 Security

- **API Key Authentication**: Simple API key authentication for development
- **Input Validation**: Pydantic models for API validation
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **CORS Configuration**: Restricted to development frontend URL

## 📈 Monitoring & Logging

### Application Logs
```bash
# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# View database logs
docker-compose logs -f postgres
```

### Health Checks
- **Backend Health**: http://localhost:8000/health
- **Database Health**: PostgreSQL connection status

## 🚀 Deployment

### Development
```bash
docker-compose up -d
```

### Production (Future)
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. Follow the AI-DLC workflow for new features
2. Ensure all tests pass
3. Update documentation
4. Use conventional commit messages

## 📝 License

[Add your license information here]

## 📞 Support

- **Documentation**: Check `.aidlc/` directory for AI-DLC workflow documentation
- **API Documentation**: http://localhost:8000/docs
- **Issues**: Create GitHub issues for bugs or feature requests