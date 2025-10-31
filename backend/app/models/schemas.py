from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


# Request Models

class QueryContext(BaseModel):
    """Context information for the query."""
    dapp: str = Field(default="kamino", description="DApp name")
    lang: str = Field(default="en", description="Language code (en, pl)")


class AskRequest(BaseModel):
    """Request model for /ask endpoint."""
    query: str = Field(..., description="User's question", min_length=1, max_length=1000)
    pool_id: Optional[str] = Field(None, description="Pool ID (e.g., 'allez-usdc')")
    amount: Optional[float] = Field(1000, description="Amount for calculations", gt=0)
    currency: Optional[str] = Field("USDC", description="Currency code")
    context: QueryContext = Field(default_factory=QueryContext)
    session_id: Optional[str] = Field(None, description="Session UUID")
    client_id: Optional[str] = Field(None, description="Client identifier for analytics")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "How much can I earn on 1000 USDC?",
                "pool_id": "allez-usdc",
                "amount": 1000,
                "currency": "USDC",
                "context": {
                    "dapp": "kamino",
                    "lang": "en"
                }
            }
        }


# Response Models

class EarningsData(BaseModel):
    """Earnings calculation data."""
    yearly: float = Field(..., description="Yearly earnings in USD")
    monthly: float = Field(..., description="Monthly earnings in USD")
    apr_value: float = Field(..., description="APR as decimal (0.124 = 12.4%)")
    updated_at: str = Field(..., description="When APR was last updated (e.g., '2 hours ago')")


class Source(BaseModel):
    """Source reference."""
    title: str = Field(..., description="Source title")
    url: str = Field(..., description="Source URL")


class QueryAssumptions(BaseModel):
    """Assumptions used for calculations."""
    pool: str = Field(..., description="Pool ID")
    amount: float = Field(..., description="Amount used")
    currency: str = Field(..., description="Currency used")


class AskResponse(BaseModel):
    """Response model for /ask endpoint."""
    answer: str = Field(..., description="Main answer text")
    earnings: Optional[EarningsData] = Field(None, description="Earnings data (for earnings queries)")
    assumptions: Optional[QueryAssumptions] = Field(None, description="Calculation assumptions")
    confidence: Optional[float] = Field(None, description="Confidence score (0.0-1.0)", ge=0, le=1)
    sources: Optional[List[Source]] = Field(None, description="Source references")
    followups: Optional[List[str]] = Field(None, description="Suggested follow-up questions")
    session_id: str = Field(..., description="Session UUID")
    dapp: str = Field(default="kamino", description="DeFi service used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Based on current rates, depositing 1,000 USDC into the Allez USDC pool can earn you approximately $124 per year.",
                "earnings": {
                    "yearly": 124.0,
                    "monthly": 10.33,
                    "apr_value": 0.124,
                    "updated_at": "2 hours ago"
                },
                "assumptions": {
                    "pool": "allez-usdc",
                    "amount": 1000,
                    "currency": "USDC"
                },
                "confidence": 0.88,
                "sources": [
                    {
                        "title": "Kamino Allez USDC Pool",
                        "url": "https://kamino.finance/lend/allez-usdc"
                    }
                ],
                "followups": [
                    "How often are rewards distributed?",
                    "What are the risks?",
                    "Can I withdraw anytime?"
                ],
                "session_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


# Admin Models

class CacheStats(BaseModel):
    """Cache statistics."""
    total_queries: int
    cached_queries: int
    cache_hit_rate: float
    total_size_mb: float
    oldest_entry: Optional[datetime]
    newest_entry: Optional[datetime]


class CacheRefreshRequest(BaseModel):
    """Request to refresh cache entries."""
    query_ids: Optional[List[str]] = Field(None, description="Specific query IDs to refresh")
    pool_id: Optional[str] = Field(None, description="Refresh all queries for a pool")
    older_than_hours: Optional[int] = Field(None, description="Refresh entries older than X hours")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(default="1.0.0")
    services: Optional[Dict[str, str]] = Field(None, description="Individual service statuses")


# Internal Models (for database)

class QueryType(str):
    """Query type classification."""
    EARNINGS = "earnings"
    GENERAL = "general"
    RISK = "risk"
    TECHNICAL = "technical"
    UNKNOWN = "unknown"
