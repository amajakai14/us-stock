import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Box,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Pagination,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip
} from '@mui/material';
import { Search, Business, Star, StarBorder } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { apiService, Company, CompanySearchParams } from '../services/api';

const CompanyListPage: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);

  // Filters
  const [exchange, setExchange] = useState('');
  const [sector, setSector] = useState('');
  const [selectedOnly, setSelectedOnly] = useState<boolean | undefined>(undefined);

  // Available filter options
  const [exchanges, setExchanges] = useState<string[]>([]);
  const [sectors, setSectors] = useState<string[]>([]);

  const pageSize = 20;

  // Load filter options on mount
  useEffect(() => {
    const loadFilters = async () => {
      try {
        const filters = await apiService.getAvailableFilters();
        setExchanges(filters.exchanges);
        setSectors(filters.sectors);
      } catch (err) {
        console.error('Failed to load filters:', err);
      }
    };

    loadFilters();
  }, []);

  // Load companies
  const loadCompanies = async () => {
    setLoading(true);
    setError(null);

    try {
      const params: CompanySearchParams = {
        query: searchQuery || undefined,
        exchange: exchange || undefined,
        sector: sector || undefined,
        is_selected: selectedOnly,
        page,
        size: pageSize
      };

      const response = await apiService.getCompanies(params);
      setCompanies(response.companies);
      setTotal(response.total);
      setTotalPages(Math.ceil(response.total / pageSize));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load companies');
      setCompanies([]);
      setTotal(0);
      setTotalPages(1);
    } finally {
      setLoading(false);
    }
  };

  // Load companies on filter/page changes
  useEffect(() => {
    loadCompanies();
  }, [searchQuery, exchange, sector, selectedOnly, page]);

  // Handle search
  const handleSearch = (event: React.FormEvent) => {
    event.preventDefault();
    setPage(1); // Reset to first page on search
  };

  // Handle company selection
  const handleSelectCompany = async (companyId: string, isSelected: boolean) => {
    try {
      await apiService.selectCompany(companyId, { selected: isSelected });
      // Reload companies to reflect the change
      loadCompanies();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update company selection');
    }
  };

  const formatMarketCap = (marketCap?: number) => {
    if (!marketCap) return 'N/A';
    if (marketCap >= 1e12) return `$${(marketCap / 1e12).toFixed(1)}T`;
    if (marketCap >= 1e9) return `$${(marketCap / 1e9).toFixed(1)}B`;
    if (marketCap >= 1e6) return `$${(marketCap / 1e6).toFixed(1)}M`;
    return `$${marketCap.toLocaleString()}`;
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Discover US Stocks
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Search and browse all active US stock tickers, then select companies to track for SEC data collection.
        </Typography>
      </Box>

      {/* Search and Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <form onSubmit={handleSearch}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  placeholder="Search by ticker or company name..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  InputProps={{
                    startAdornment: <Search sx={{ mr: 1, color: 'action.active' }} />
                  }}
                />
              </Grid>

              <Grid item xs={12} md={2}>
                <FormControl fullWidth>
                  <InputLabel>Exchange</InputLabel>
                  <Select
                    value={exchange}
                    label="Exchange"
                    onChange={(e) => setExchange(e.target.value)}
                  >
                    <MenuItem value="">All Exchanges</MenuItem>
                    {exchanges.map((ex) => (
                      <MenuItem key={ex} value={ex}>{ex}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={2}>
                <FormControl fullWidth>
                  <InputLabel>Sector</InputLabel>
                  <Select
                    value={sector}
                    label="Sector"
                    onChange={(e) => setSector(e.target.value)}
                  >
                    <MenuItem value="">All Sectors</MenuItem>
                    {sectors.map((sec) => (
                      <MenuItem key={sec} value={sec}>{sec}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={2}>
                <FormControl fullWidth>
                  <InputLabel>Filter</InputLabel>
                  <Select
                    value={selectedOnly === undefined ? '' : selectedOnly.toString()}
                    label="Filter"
                    onChange={(e) => {
                      const value = e.target.value;
                      setSelectedOnly(value === '' ? undefined : value === 'true');
                    }}
                  >
                    <MenuItem value="">All Companies</MenuItem>
                    <MenuItem value="true">Selected Only</MenuItem>
                    <MenuItem value="false">Not Selected</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={2}>
                <Button type="submit" variant="contained" fullWidth>
                  Search
                </Button>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>

      {/* Navigation */}
      <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
        <Button component={Link} to="/selections" variant="outlined">
          View Selections ({companies.filter(c => c.is_selected).length})
        </Button>
        <Button component={Link} to="/schedules" variant="outlined">
          Manage Schedules
        </Button>
      </Box>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Results Summary */}
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          Showing {companies.length} of {total} companies
        </Typography>
      </Box>

      {/* Loading */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Company List */}
      {!loading && (
        <Grid container spacing={2}>
          {companies.map((company) => (
            <Grid item xs={12} sm={6} md={4} key={company.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Business color="primary" />
                      <Typography variant="h6" component="h2">
                        {company.ticker_symbol}
                      </Typography>
                    </Box>
                    <Tooltip title={company.is_selected ? 'Deselect company' : 'Select company'}>
                      <IconButton
                        onClick={() => handleSelectCompany(company.id, !company.is_selected)}
                        color={company.is_selected ? 'primary' : 'default'}
                      >
                        {company.is_selected ? <Star /> : <StarBorder />}
                      </IconButton>
                    </Tooltip>
                  </Box>

                  <Typography variant="body1" sx={{ mb: 1, fontWeight: 'medium' }}>
                    {company.company_name}
                  </Typography>

                  <Box sx={{ mb: 1 }}>
                    <Chip
                      label={company.exchange}
                      size="small"
                      variant="outlined"
                      sx={{ mr: 1 }}
                    />
                    {company.sector && (
                      <Chip
                        label={company.sector}
                        size="small"
                        variant="outlined"
                        sx={{ mr: 1 }}
                      />
                    )}
                  </Box>

                  <Typography variant="body2" color="text.secondary">
                    Market Cap: {formatMarketCap(company.market_cap)}
                  </Typography>

                  {company.selection_date && (
                    <Typography variant="caption" color="primary" sx={{ mt: 1, display: 'block' }}>
                      Selected: {new Date(company.selection_date).toLocaleDateString()}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Pagination */}
      {!loading && totalPages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={(_, newPage) => setPage(newPage)}
            color="primary"
          />
        </Box>
      )}

      {/* No Results */}
      {!loading && companies.length === 0 && !error && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No companies found
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Try adjusting your search or filters
          </Typography>
        </Box>
      )}
    </Container>
  );
};

export default CompanyListPage;