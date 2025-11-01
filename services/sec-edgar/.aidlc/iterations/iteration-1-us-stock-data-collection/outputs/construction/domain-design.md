# Domain Design: US Stock Data Collection System - All Bounded Contexts

## 1. Domain Overview

**Bounded Contexts**: Stock Discovery, Data Collection, Data Management
**Core Domain Focus**: US stock data collection from SEC Edgar with time-series management
**Context Boundaries**: Clear separation between company discovery, automated collection, and data management capabilities

## 2. Shared Value Objects (Across All Contexts)

### TickerSymbol
**Purpose**: Immutable representation of stock ticker symbols
**Immutability**: Ticker symbols never change and should be validated at creation

**Properties**:
- `symbol`: str - The ticker symbol (e.g., "AAPL", "GOOGL")

**Validation Rules**:
- Must be 1-5 characters
- Must contain only uppercase letters
- Must be a valid stock ticker format

---

### DateRange
**Purpose**: Immutable representation of date ranges for filtering and queries
**Immutability**: Date ranges should not be modified once created

**Properties**:
- `startDate`: datetime - Start of the range (inclusive)
- `endDate`: datetime - End of the range (inclusive)

**Validation Rules**:
- startDate must be <= endDate
- Both dates must be valid datetime objects
- Range cannot exceed 10 years for performance reasons

---

### Money
**Purpose**: Immutable representation of monetary values
**Immutability**: Monetary values should not be modified, new instances created for changes

**Properties**:
- `amount`: Decimal - The monetary amount
- `currency`: str - Currency code (e.g., "USD")

**Validation Rules**:
- amount must be non-negative for most business contexts
- currency must be a valid ISO 4217 code
- precision limited to 2 decimal places for USD

---

## 3. Stock Discovery Context

### Company (Aggregate Root)
**Type**: Aggregate Root
**Purpose**: Central entity representing a public company available for tracking
**Identity**: Unique company identifier (UUID)

**Attributes**:
- `id`: UUID - Unique identifier
- `tickerSymbol`: TickerSymbol - Stock ticker symbol
- `companyName`: str - Full company name
- `exchange`: str - Stock exchange (e.g., "NASDAQ", "NYSE")
- `sector`: str - Industry sector
- `marketCap`: Money - Market capitalization
- `isSelected`: bool - Whether this company is selected for data collection
- `selectionDate`: datetime - When company was selected for tracking
- `createdAt`: datetime - When this record was created
- `updatedAt`: datetime - When this record was last updated

**Business Rules**:
- A company can only be selected if it has a valid ticker symbol
- Once selected, selection date cannot be changed
- Company name and ticker symbol combination must be unique

**Invariants**:
- Ticker symbol must always be valid
- Selected status must be consistent with selection date
- Market cap must be non-negative

**Business Operations**:
- `selectForTracking()`: Marks company for data collection
- `deselectFromTracking()`: Removes company from data collection
- `updateCompanyInfo(name, exchange, sector, marketCap)`: Updates company metadata
- `isValidForSelection()`: Checks if company meets criteria for selection

---

## 4. Data Collection Context

### CollectionSchedule (Aggregate Root)
**Type**: Aggregate Root
**Purpose**: Manages when and how often to collect data for selected companies
**Identity**: Unique schedule identifier (UUID)

**Attributes**:
- `id`: UUID - Unique identifier
- `companyId`: UUID - Reference to Company aggregate
- `scheduleType`: str - Type of schedule ("DAILY", "WEEKLY", "MONTHLY")
- `intervalHours`: int - Hours between collections
- `nextRunTime`: datetime - When next collection should run
- `lastRunTime`: datetime - When last collection was attempted
- `isActive`: bool - Whether this schedule is currently active
- `filingTypes`: List[str] - Types of SEC filings to collect
- `createdAt`: datetime - Schedule creation time
- `updatedAt`: datetime - Last schedule update

**Business Rules**:
- Schedule can only be created for selected companies
- Interval must be at least 1 hour for API rate limiting
- Only one active schedule per company per filing type

**Invariants**:
- Active schedules must have valid nextRunTime
- Schedule type must match intervalHours
- Filing types must be valid SEC filing codes

**Business Operations**:
- `activateSchedule()`: Enables the schedule for execution
- `deactivateSchedule()`: Disables the schedule
- `updateNextRunTime()`: Calculates next collection time
- `canRunNow()`: Checks if schedule is ready for execution
- `markExecutionCompleted()`: Updates lastRunTime and calculates next run

---

### SECData (Entity)
**Type**: Entity
**Purpose**: Represents collected SEC filing data for a company
**Identity**: Composite of companyId + filingDate + filingType + accessionNumber

**Attributes**:
- `id`: UUID - Unique identifier
- `companyId`: UUID - Reference to Company
- `filingType`: str - SEC filing type (10-K, 10-Q, 8-K, etc.)
- `filingDate`: datetime - Official SEC filing date
- `accessionNumber`: str - SEC accession number
- `dataContent`: dict - Parsed filing content
- `rawContent`: str - Original filing content
- `collectionTimestamp`: datetime - When we collected this data
- `processingStatus`: str - Status of data processing
- `createdAt`: datetime - Record creation time

**Business Rules**:
- Filing data can only be created for selected companies
- Accession numbers must be unique across all filings
- Processing status must follow proper state transitions

**Invariants**:
- Filing date cannot be in the future
- Accession number must match SEC format
- Collection timestamp must be after filing date

---

### FinancialReportDates (Entity)
**Type**: Entity
**Purpose**: Tracks expected and actual financial report dates for companies
**Identity**: Composite of companyId + reportType + fiscalYear

**Attributes**:
- `id`: UUID - Unique identifier
- `companyId`: UUID - Reference to Company
- `reportType`: str - Type of report ("ANNUAL", "QUARTERLY")
- `fiscalYear`: int - Fiscal year
- `fiscalQuarter`: int - Fiscal quarter (for quarterly reports)
- `expectedDate`: datetime - Expected filing date based on patterns
- `actualDate`: datetime - Actual filing date when filed
- `isFiled`: bool - Whether the report has been filed
- `daysPastDue`: int - Days past expected date if not filed
- `createdAt`: datetime - Record creation time
- `updatedAt`: datetime - Last update time

**Business Rules**:
- Expected dates calculated based on company historical patterns
- Quarterly reports only relevant for quarterly report types
- Days past due calculated daily until filed

**Invariants**:
- Fiscal year must be current or within reasonable range
- Fiscal quarter must be 1-4 for quarterly reports
- Actual date cannot be before expected date

---

## 5. Data Management Context

### TimeSeriesData (Entity)
**Type**: Entity
**Purpose**: Time-series data for analysis and historical tracking
**Identity**: Composite of companyId + dataType + timestamp

**Attributes**:
- `id`: UUID - Unique identifier
- `companyId`: UUID - Reference to Company
- `dataType`: str - Type of time-series data
- `timestamp`: datetime - Data timestamp
- `value`: Decimal - Data value
- `metadata`: dict - Additional data context
- `source`: str - Data source identifier
- `createdAt`: datetime - Record creation time

**Business Rules**:
- Time-series data only created for selected companies
- Values must be numeric for proper time-series analysis
- Timestamp precision to minute level for most data

**Invariants**:
- Timestamp cannot be in the future for most data types
- Value must be finite (not infinity or NaN)
- Source must be a valid data source identifier

---

### DataExport (Aggregate Root)
**Type**: Aggregate Root
**Purpose**: Manages export requests and execution for collected data
**Identity**: Unique export identifier (UUID)

**Attributes**:
- `id`: UUID - Unique identifier
- `companyId`: UUID - Company to export data for (null for all companies)
- `dateRange`: DateRange - Date range for export
- `exportFormat`: str - Export format ("CSV", "JSON", "EXCEL")
- `dataTypes`: List[str] - Types of data to include
- `status`: str - Export status ("PENDING", "PROCESSING", "COMPLETED", "FAILED")
- `filePath`: str - Path to generated export file
- `fileSize`: int - Size of generated file in bytes
- `recordCount`: int - Number of records exported
- `errorMessage`: str - Error message if export failed
- `requestedAt`: datetime - When export was requested
- `completedAt`: datetime - When export completed
- `createdAt`: datetime - Record creation time

**Business Rules**:
- Exports can only be requested for selected companies
- Date range cannot exceed retention policy limits
- Export format must be supported by the system

**Invariants**:
- File size and record count must be non-negative
- Status transitions must follow proper sequence
- Completed date only set when status is COMPLETED or FAILED

**Business Operations**:
- `startProcessing()`: Marks export as being processed
- `completeExport(filePath, fileSize, recordCount)`: Marks export as completed
- `failExport(errorMessage)`: Marks export as failed
- `canBeProcessed()`: Checks if export is ready for processing

---

## 6. Domain Events

### CompanySelectionChanged
**Trigger**: Company is selected or deselected for tracking
**Purpose**: Notify Data Collection context to start/stop scheduling
**Data**: Company ID, new selection status, selection date

**Event Structure**:
```
CompanySelectionChanged {
  eventId: UUID
  aggregateId: UUID (companyId)
  timestamp: DateTime
  isSelected: bool
  selectionDate: DateTime
}
```

---

### DataCollected
**Trigger**: New SEC data successfully collected for a company
**Purpose**: Notify Data Management context of new data availability
**Data**: Company ID, filing type, filing date, collection timestamp

**Event Structure**:
```
DataCollected {
  eventId: UUID
  aggregateId: UUID (companyId)
  timestamp: DateTime
  filingType: str
  filingDate: DateTime
  accessionNumber: str
  collectionTimestamp: DateTime
}
```

---

### ExportRequested
**Trigger**: User requests data export
**Purpose**: Trigger export processing in background
**Data**: Export ID, company ID, date range, format, data types

**Event Structure**:
```
ExportRequested {
  eventId: UUID
  aggregateId: UUID (exportId)
  timestamp: DateTime
  companyId: UUID
  dateRange: DateRange
  exportFormat: str
  dataTypes: List[str]
}
```

---

## 7. Domain Services

### SECDataFetchService
**Purpose**: Handles communication with SEC Edgar API
**Operations**:
- `fetchCompanyFilings(tickerSymbol, filingTypes, dateRange)`: Fetch filings from SEC
- `parseFilingData(rawContent)`: Parse raw SEC filing content
- `validateFilingData(parsedData)`: Validate parsed data structure

**Dependencies**: SEC Edgar API client, data parsing utilities

---

### ScheduleCalculationService
**Purpose**: Calculates optimal collection schedules
**Operations**:
- `calculateNextRunTime(scheduleType, intervalHours, lastRunTime)`: Calculate next collection time
- `optimizeScheduleForCompany(company, filingTypes)`: Suggest optimal schedule
- `validateScheduleConstraints(schedule)`: Validate schedule doesn't violate constraints

**Dependencies**: Calendar utilities, business rule engine

---

### DataRetentionService
**Purpose**: Manages rolling window data retention policies
**Operations**:
- `calculateRetentionData(dataType, collectionDate)`: Determine if data should be retained
- `purgeExpiredData(companyId, retentionPolicy)`: Remove expired data
- `archiveOldData(companyId, archiveThreshold)`: Archive old data

**Dependencies**: Time utilities, storage management

---

## 8. Business Rules (Pseudocode)

### Company Selection Process
```
WHEN user requests to select company
VALIDATE company has valid ticker symbol
IF company is not already selected
  THEN company.selectForTracking()
  AND company.updateSelectionDate(currentTime)
  AND EMIT CompanySelectionChanged(isSelected=true, selectionDate)
ELSE
  THROW CompanyAlreadySelectedException
END
```

### Data Collection Scheduling
```
WHEN schedule execution is triggered
VALIDATE schedule.isActive AND schedule.canRunNow()
IF valid
  THEN collectSECData(schedule.companyId, schedule.filingTypes)
  AND schedule.markExecutionCompleted()
  AND EMIT DataCollected(filingData)
ELSE
  THROW ScheduleNotReadyException
END
```

### Export Request Processing
```
WHEN user requests data export
VALIDATE user has permission for requested data
VALIDATE dateRange within retention policy
IF valid
  THEN create DataExport(request details)
  AND EMIT ExportRequested(export details)
ELSE
  THROW ExportValidationException
END
```

---

## 9. Repository Interfaces

### CompanyRepository
**Purpose**: Data access for Company aggregate
**Operations**:
- `findById(id)`: Find company by identifier
- `findByTickerSymbol(tickerSymbol)`: Find company by ticker
- `findSelectedCompanies()`: Find all companies selected for tracking
- `save(company)`: Persist company changes
- `delete(id)`: Remove company

---

### CollectionScheduleRepository
**Purpose**: Data access for CollectionSchedule aggregate
**Operations**:
- `findById(id)`: Find schedule by identifier
- `findByCompanyId(companyId)`: Find schedules for a company
- `findActiveSchedules()`: Find all active schedules
- `findSchedulesReadyToRun()`: Find schedules ready for execution
- `save(schedule)`: Persist schedule changes
- `delete(id)`: Remove schedule

---

### SECDataRepository
**Purpose**: Data access for SEC data entities
**Operations**:
- `findById(id)`: Find SEC data by identifier
- `findByCompanyAndDateRange(companyId, dateRange)`: Find data for company in date range
- `findByFilingType(companyId, filingType, dateRange)`: Find specific filing types
- `findLatestFiling(companyId, filingType)`: Find most recent filing
- `save(secData)`: Persist SEC data
- `delete(id)`: Remove SEC data

---

### DataExportRepository
**Purpose**: Data access for DataExport aggregate
**Operations**:
- `findById(id)`: Find export by identifier
- `findByStatus(status)`: Find exports by status
- `findByCompanyId(companyId)`: Find exports for a company
- `save(export)`: Persist export changes
- `delete(id)`: Remove export

---

## 10. Integration Points

### Inbound Dependencies
- **React Frontend**: Company selection, schedule configuration, export requests
- **External Data Sources**: Initial company list from stock exchange data
- **System Clock**: For schedule calculations and timestamps

### Outbound Dependencies
- **SEC Edgar API**: Primary source for company filing data
- **File System**: Export file storage and retrieval
- **Background Scheduler**: For automated data collection execution

---

## 11. SQLAlchemy Model Considerations

### Database Schema Design
- **Companies Table**: Core company information with selected flag
- **Collection_Schedules Table**: Schedule configuration and next run times
- **SEC_Data Table**: Filing data with JSONB for flexible content storage
- **Financial_Report_Dates Table**: Expected and actual report date tracking
- **Time_Series_Data Table**: Optimized for time queries with proper indexing
- **Data_Exports Table**: Export request tracking and status

### Performance Optimization
- Proper indexing on ticker symbols, company IDs, and timestamps
- JSONB columns for flexible SEC data storage
- Partitioning considerations for time-series data
- Query optimization for date range searches

---

## 12. Success Criteria

- [x] All entities have clear business purpose and identity
- [x] Value objects are properly immutable with validation
- [x] Aggregates maintain consistency boundaries
- [x] Domain events capture important business moments
- [x] Business rules are expressed in pseudocode
- [x] Repository interfaces defined for data access
- [x] Integration points with other contexts specified
- [x] SQLAlchemy considerations documented for implementation