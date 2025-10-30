from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

# API Key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """
    Verify API key from request header.
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        Validated API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    # Parse comma-separated API keys from settings
    valid_keys = [key.strip() for key in settings.api_keys]
    
    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    
    return api_key


async def verify_admin_api_key(api_key: str = Security(verify_api_key)) -> str:
    """
    Verify admin API key (for admin endpoints).
    Currently uses same keys, but can be extended for role-based access.
    
    Args:
        api_key: Validated API key
        
    Returns:
        Validated admin API key
    """
    # TODO: Implement role-based access control
    # For now, all valid API keys have admin access
    return api_key
