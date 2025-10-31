from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
import uuid

from app.core.database import Base


class Document(Base):
    """
    Document storage with vector embeddings for RAG.
    Stores scraped documentation from Kamino and other sources.
    """
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String(1000), nullable=False)
    dapp = Column(String(100), nullable=False, default="kamino")
    doc_type = Column(String(50), nullable=False, default="documentation")
    
    # Vector embedding for semantic search
    embedding = Column(Vector(384), nullable=True)  # Dimension depends on model
    
    # Metadata (using 'name' to avoid conflict with SQLAlchemy's metadata attribute)
    meta_data = Column('metadata', JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_documents_dapp', 'dapp'),
        Index('idx_documents_doc_type', 'doc_type'),
        Index('idx_documents_embedding', 'embedding', postgresql_using='ivfflat'),
    )


class QueryCache(Base):
    """
    Cache for query responses with semantic similarity search.
    Stores LLM responses to avoid redundant API calls.
    """
    __tablename__ = "query_cache"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Query information
    query_text = Column(Text, nullable=False)
    query_embedding = Column(Vector(384), nullable=False)
    query_type = Column(String(50), nullable=False)  # earnings, general, risk, etc.
    
    # DeFi service context
    dapp = Column(String(100), nullable=False, default="kamino")  # kamino, aave, compound, etc.
    
    # Pool information (if applicable)
    pool_id = Column(String(100), nullable=True)
    amount = Column(Float, nullable=True)
    currency = Column(String(20), nullable=True)
    
    # Client tracking
    client_id = Column(String(255), nullable=True)  # Client identifier for analytics
    
    # Response data
    response_json = Column(JSONB, nullable=False)
    
    # Metadata
    confidence = Column(Float, nullable=True)
    llm_provider = Column(String(50), nullable=False)
    llm_model = Column(String(100), nullable=False)
    
    # Usage statistics
    use_count = Column(Integer, default=1, nullable=False)
    last_used_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_query_cache_pool_id', 'pool_id'),
        Index('idx_query_cache_query_type', 'query_type'),
        Index('idx_query_cache_dapp', 'dapp'),
        Index('idx_query_cache_client_id', 'client_id'),
        Index('idx_query_cache_embedding', 'query_embedding', postgresql_using='ivfflat'),
        Index('idx_query_cache_last_used', 'last_used_at'),
    )


class APRData(Base):
    """
    Cached APR data from DeFi protocols.
    Refreshed periodically to avoid excessive API calls.
    """
    __tablename__ = "apr_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # DeFi service
    dapp = Column(String(100), nullable=False, default="kamino")  # kamino, aave, compound, etc.
    
    # Pool information
    pool_id = Column(String(100), nullable=False)
    pool_name = Column(String(200), nullable=True)
    
    # APR values
    apr_value = Column(Float, nullable=False)
    apy_value = Column(Float, nullable=True)
    
    # Additional data
    tvl = Column(Float, nullable=True)
    meta_data = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_apr_data_dapp_pool', 'dapp', 'pool_id', unique=True),
        Index('idx_apr_data_pool_id', 'pool_id'),
        Index('idx_apr_data_dapp', 'dapp'),
        Index('idx_apr_data_updated_at', 'updated_at'),
    )


class Session(Base):
    """
    User session tracking.
    Stores conversation history and context.
    """
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Client tracking
    client_id = Column(String(255), nullable=True)  # Client identifier
    dapp = Column(String(100), nullable=False, default="kamino")  # DeFi service
    
    # Session data
    session_data = Column(JSONB, nullable=True)
    
    # Statistics
    query_count = Column(Integer, default=0, nullable=False)
    last_query = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_activity_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_sessions_last_activity', 'last_activity_at'),
        Index('idx_sessions_client_id', 'client_id'),
        Index('idx_sessions_dapp', 'dapp'),
    )


class QueryLog(Base):
    """
    Log all queries for analytics and monitoring.
    """
    __tablename__ = "query_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Query information
    session_id = Column(UUID(as_uuid=True), nullable=True)
    client_id = Column(String(255), nullable=True)  # Client identifier
    dapp = Column(String(100), nullable=False, default="kamino")  # DeFi service
    query_text = Column(Text, nullable=False)
    query_type = Column(String(50), nullable=True)
    
    # Response information
    response_time_ms = Column(Integer, nullable=False)
    was_cached = Column(Integer, default=0, nullable=False)  # 0 or 1 (boolean)
    confidence = Column(Float, nullable=True)
    
    # LLM usage
    llm_provider = Column(String(50), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    
    # API key (hashed for security)
    api_key_hash = Column(String(64), nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_query_logs_created_at', 'created_at'),
        Index('idx_query_logs_session_id', 'session_id'),
        Index('idx_query_logs_client_id', 'client_id'),
        Index('idx_query_logs_dapp', 'dapp'),
        Index('idx_query_logs_query_type', 'query_type'),
    )
