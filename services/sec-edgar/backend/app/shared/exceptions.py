from fastapi import HTTPException

class BaseAPIException(HTTPException):
    """Base exception for API errors"""
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)

class CompanyNotFoundError(BaseAPIException):
    """Raised when a company is not found"""
    def __init__(self, detail: str = "Company not found"):
        super().__init__(detail=detail, status_code=404)

class CompanyAlreadyExistsError(BaseAPIException):
    """Raised when trying to create a company that already exists"""
    def __init__(self, detail: str = "Company already exists"):
        super().__init__(detail=detail, status_code=409)

class ValidationError(BaseAPIException):
    """Raised when validation fails"""
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(detail=detail, status_code=422)

class ExternalAPIError(BaseAPIException):
    """Raised when external API calls fail"""
    def __init__(self, detail: str = "External API error"):
        super().__init__(detail=detail, status_code=502)