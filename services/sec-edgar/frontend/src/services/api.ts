import axios, { AxiosInstance, AxiosResponse } from 'axios';

// API configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
const API_KEY = process.env.REACT_APP_API_KEY || 'dev-api-key-12345';

// Types for API responses
export interface Company {
  id: string;
  ticker_symbol: string;
  company_name: string;
  exchange: string;
  sector?: string;
  market_cap?: number;
  is_selected: boolean;
  selection_date?: string;
  created_at: string;
  updated_at?: string;
}

export interface CompanyListResponse {
  companies: Company[];
  total: number;
  page: number;
  size: number;
}

export interface CompanySelectionRequest {
  selected: boolean;
  notes?: string;
}

export interface CompanySelectionResponse {
  company_id: string;
  selected: boolean;
  selection_date?: string;
  message: string;
}

export interface CompanySearchParams {
  query?: string;
  exchange?: string;
  sector?: string;
  is_selected?: boolean;
  page?: number;
  size?: number;
}

// Create axios instance with default configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API Service class
class ApiService {
  // Company endpoints
  async getCompanies(params?: CompanySearchParams): Promise<CompanyListResponse> {
    const response = await apiClient.get<CompanyListResponse>('/companies', { params });
    return response.data;
  }

  async searchCompanies(query: string, limit: number = 10): Promise<Company[]> {
    const response = await apiClient.get<Company[]>('/companies/search', {
      params: { q: query, limit }
    });
    return response.data;
  }

  async getSelectedCompanies(): Promise<Company[]> {
    const response = await apiClient.get<Company[]>('/companies/selected');
    return response.data;
  }

  async getAvailableFilters(): Promise<{ exchanges: string[]; sectors: string[] }> {
    const response = await apiClient.get<{ exchanges: string[]; sectors: string[] }>('/companies/filters');
    return response.data;
  }

  async getCompany(companyId: string): Promise<Company> {
    const response = await apiClient.get<Company>(`/companies/${companyId}`);
    return response.data;
  }

  async createCompany(companyData: Partial<Company>): Promise<Company> {
    const response = await apiClient.post<Company>('/companies', companyData);
    return response.data;
  }

  async updateCompany(companyId: string, updateData: Partial<Company>): Promise<Company> {
    const response = await apiClient.put<Company>(`/companies/${companyId}`, updateData);
    return response.data;
  }

  async selectCompany(companyId: string, selection: CompanySelectionRequest): Promise<CompanySelectionResponse> {
    const response = await apiClient.post<CompanySelectionResponse>(`/companies/${companyId}/select`, selection);
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await apiClient.get<{ status: string }>('/health');
    return response.data;
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;