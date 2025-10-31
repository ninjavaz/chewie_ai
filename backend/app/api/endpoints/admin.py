"""
Admin endpoints for cache management and monitoring.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_admin_api_key
from app.models.schemas import CacheStats, CacheRefreshRequest
from app.services.cache_service import get_cache_service

router = APIRouter()


@router.get("/admin/cache/stats", response_model=CacheStats)
async def get_cache_stats(
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_admin_api_key),
):
    """Get cache statistics."""
    cache_service = get_cache_service()
    stats = await cache_service.get_cache_stats(db)
    
    # Calculate cache hit rate (would need QueryLog table for accurate stats)
    total_queries = stats.get("total_queries", 0)
    cached_queries = total_queries  # Placeholder
    cache_hit_rate = 0.0 if total_queries == 0 else cached_queries / total_queries
    
    return CacheStats(
        total_queries=total_queries,
        cached_queries=cached_queries,
        cache_hit_rate=round(cache_hit_rate, 2),
        total_size_mb=0.0,  # TODO: Calculate actual size
        oldest_entry=stats.get("oldest_entry"),
        newest_entry=stats.get("newest_entry"),
    )


@router.post("/admin/cache/refresh")
async def refresh_cache(
    request: CacheRefreshRequest,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_admin_api_key),
):
    """Refresh cache entries."""
    cache_service = get_cache_service()
    
    deleted_count = await cache_service.invalidate_cache(
        db=db,
        pool_id=request.pool_id,
        older_than_hours=request.older_than_hours,
    )
    
    return {
        "status": "success",
        "deleted_entries": deleted_count,
        "message": f"Invalidated {deleted_count} cache entries"
    }


@router.delete("/admin/cache/clear")
async def clear_cache(
    pool_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_admin_api_key),
):
    """Clear all or specific cache entries."""
    cache_service = get_cache_service()
    
    deleted_count = await cache_service.invalidate_cache(
        db=db,
        pool_id=pool_id,
    )
    
    return {
        "status": "success",
        "deleted_entries": deleted_count,
        "message": f"Cleared {deleted_count} cache entries"
    }


@router.get("/admin/metrics")
async def get_metrics(
    api_key: str = Depends(verify_admin_api_key),
):
    """Get Prometheus-style metrics."""
    # TODO: Implement proper Prometheus metrics
    return {
        "status": "ok",
        "message": "Metrics endpoint - implement Prometheus integration"
    }
