"""
Cache service for storing and retrieving query responses.
Uses both PostgreSQL (for semantic search) and Redis (for fast lookups).
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json
import hashlib
from sqlalchemy import select, func, update, cast, Text, literal, type_coerce, text
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.models.database import QueryCache
from app.models.schemas import AskResponse
from app.utils.embeddings import get_embedding_service
from app.core.redis import get_redis


class CacheService:
    """Service for caching query responses."""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
    
    async def get_cached_response(
        self,
        query: str,
        db: AsyncSession,
        dapp: str = "kamino",
        similarity_threshold: float = 0.95,
        max_age_seconds: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached response for a query using semantic similarity.
        
        Args:
            query: User's query
            db: Database session
            dapp: DeFi service name
            similarity_threshold: Minimum similarity for cache hit
            max_age_seconds: Maximum age of cached entry in seconds
            
        Returns:
            Cached response or None
        """
        # Generate query embedding
        query_embedding = self.embedding_service.encode(query)
        
        # Convert to pgvector format: "[1,2,3]"
        embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
        
        # Use text() to create a raw SQL expression that bypasses pgvector validation
        embedding_literal = text(f"'{embedding_str}'::vector")
        
        # Build query
        stmt = (
            select(
                QueryCache,
                (1 - func.cosine_distance(QueryCache.query_embedding, embedding_literal)).label("similarity")
            )
            .where(QueryCache.query_embedding.isnot(None))
            .where(QueryCache.dapp == dapp)  # Filter by DeFi service
            .order_by(func.cosine_distance(QueryCache.query_embedding, embedding_literal))
            .limit(1)
        )
        
        # Apply age filter if specified
        if max_age_seconds:
            cutoff_time = datetime.utcnow() - timedelta(seconds=max_age_seconds)
            stmt = stmt.where(QueryCache.updated_at >= cutoff_time)
        
        result = await db.execute(stmt)
        row = result.first()
        
        if not row:
            return None
        
        cache_entry, similarity = row
        
        # Check if similarity meets threshold
        if similarity < similarity_threshold:
            return None
        
        # Update usage statistics
        await self._update_cache_stats(cache_entry.id, db)
        
        # Return cached response
        response_data = cache_entry.response_json
        response_data["_cached"] = True
        response_data["_cache_similarity"] = float(similarity)
        
        return response_data
    
    async def save_response(
        self,
        query: str,
        response: AskResponse,
        db: AsyncSession,
        dapp: str = "kamino",
        query_type: str = "general",
        pool_id: Optional[str] = None,
        amount: Optional[float] = None,
        currency: Optional[str] = None,
        client_id: Optional[str] = None,
        llm_provider: str = "openai",
        llm_model: str = "gpt-4",
        confidence: Optional[float] = None,
    ) -> QueryCache:
        """
        Save query response to cache.
        
        Args:
            query: User's query
            response: Generated response
            db: Database session
            dapp: DeFi service name
            query_type: Type of query
            pool_id: Pool ID if applicable
            amount: Amount if applicable
            currency: Currency if applicable
            client_id: Client identifier
            llm_provider: LLM provider used
            llm_model: LLM model used
            confidence: Confidence score
            
        Returns:
            Created QueryCache entry
        """
        # Generate query embedding
        query_embedding = self.embedding_service.encode(query)
        
        # Convert response to dict
        response_dict = response.model_dump()
        
        # Create cache entry
        cache_entry = QueryCache(
            query_text=query,
            query_embedding=query_embedding,
            query_type=query_type,
            dapp=dapp,
            pool_id=pool_id,
            amount=amount,
            currency=currency,
            client_id=client_id,
            response_json=response_dict,
            confidence=confidence,
            llm_provider=llm_provider,
            llm_model=llm_model,
            use_count=1,
            last_used_at=datetime.utcnow(),
        )
        
        db.add(cache_entry)
        await db.flush()
        
        # Also cache in Redis for fast exact lookups
        await self._cache_in_redis(query, response_dict)
        
        return cache_entry
    
    async def _update_cache_stats(self, cache_id: str, db: AsyncSession) -> None:
        """Update cache entry usage statistics."""
        stmt = (
            update(QueryCache)
            .where(QueryCache.id == cache_id)
            .values(
                use_count=QueryCache.use_count + 1,
                last_used_at=datetime.utcnow(),
            )
        )
        await db.execute(stmt)
    
    async def _cache_in_redis(
        self,
        query: str,
        response: Dict[str, Any],
        ttl_hours: int = 24,
    ) -> None:
        """Cache response in Redis for fast exact lookups."""
        try:
            redis = await get_redis()
            
            # Create cache key from query hash
            query_hash = hashlib.sha256(query.lower().encode()).hexdigest()
            cache_key = f"query_cache:{query_hash}"
            
            # Store in Redis with TTL
            await redis.setex(
                cache_key,
                ttl_hours * 3600,
                json.dumps(response),
            )
        except Exception as e:
            # Redis failures shouldn't break the application
            print(f"Redis cache error: {e}")
    
    async def get_from_redis(self, query: str) -> Optional[Dict[str, Any]]:
        """Get cached response from Redis (exact match)."""
        try:
            redis = await get_redis()
            
            query_hash = hashlib.sha256(query.lower().encode()).hexdigest()
            cache_key = f"query_cache:{query_hash}"
            
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            print(f"Redis get error: {e}")
        
        return None
    
    async def invalidate_cache(
        self,
        db: AsyncSession,
        pool_id: Optional[str] = None,
        older_than_hours: Optional[int] = None,
    ) -> int:
        """
        Invalidate cache entries.
        
        Args:
            db: Database session
            pool_id: Invalidate entries for specific pool
            older_than_hours: Invalidate entries older than X hours
            
        Returns:
            Number of entries deleted
        """
        from sqlalchemy import delete
        
        stmt = delete(QueryCache)
        
        if pool_id:
            stmt = stmt.where(QueryCache.pool_id == pool_id)
        
        if older_than_hours:
            cutoff_time = datetime.utcnow() - timedelta(hours=older_than_hours)
            stmt = stmt.where(QueryCache.updated_at < cutoff_time)
        
        result = await db.execute(stmt)
        await db.commit()
        
        return result.rowcount
    
    async def get_cache_stats(self, db: AsyncSession) -> Dict[str, Any]:
        """Get cache statistics."""
        from sqlalchemy import func as sql_func
        
        # Total queries
        total_stmt = select(sql_func.count(QueryCache.id))
        total_result = await db.execute(total_stmt)
        total_queries = total_result.scalar() or 0
        
        # Most used queries
        popular_stmt = (
            select(QueryCache.query_text, QueryCache.use_count)
            .order_by(QueryCache.use_count.desc())
            .limit(5)
        )
        popular_result = await db.execute(popular_stmt)
        popular_queries = [
            {"query": row[0], "use_count": row[1]}
            for row in popular_result.all()
        ]
        
        # Oldest and newest entries
        oldest_stmt = select(sql_func.min(QueryCache.created_at))
        oldest_result = await db.execute(oldest_stmt)
        oldest_entry = oldest_result.scalar()
        
        newest_stmt = select(sql_func.max(QueryCache.created_at))
        newest_result = await db.execute(newest_stmt)
        newest_entry = newest_result.scalar()
        
        return {
            "total_queries": total_queries,
            "popular_queries": popular_queries,
            "oldest_entry": oldest_entry.isoformat() if oldest_entry else None,
            "newest_entry": newest_entry.isoformat() if newest_entry else None,
        }


# Global instance
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """Get or create CacheService instance."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
