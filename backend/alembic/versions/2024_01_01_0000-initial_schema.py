"""Initial schema with pgvector support

Revision ID: initial_schema
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = 'initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('url', sa.String(1000), nullable=False),
        sa.Column('dapp', sa.String(100), nullable=False, server_default='kamino'),
        sa.Column('doc_type', sa.String(50), nullable=False, server_default='documentation'),
        sa.Column('embedding', Vector(384), nullable=True),
        sa.Column('metadata', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )
    
    op.create_index('idx_documents_dapp', 'documents', ['dapp'])
    op.create_index('idx_documents_doc_type', 'documents', ['doc_type'])
    op.create_index('idx_documents_embedding', 'documents', ['embedding'], postgresql_using='ivfflat')
    
    # Create query_cache table
    op.create_table(
        'query_cache',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('query_text', sa.Text(), nullable=False),
        sa.Column('query_embedding', Vector(384), nullable=False),
        sa.Column('query_type', sa.String(50), nullable=False),
        sa.Column('pool_id', sa.String(100), nullable=True),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(20), nullable=True),
        sa.Column('response_json', JSONB, nullable=False),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('llm_provider', sa.String(50), nullable=False),
        sa.Column('llm_model', sa.String(100), nullable=False),
        sa.Column('use_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('last_used_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )
    
    op.create_index('idx_query_cache_pool_id', 'query_cache', ['pool_id'])
    op.create_index('idx_query_cache_query_type', 'query_cache', ['query_type'])
    op.create_index('idx_query_cache_embedding', 'query_cache', ['query_embedding'], postgresql_using='ivfflat')
    op.create_index('idx_query_cache_last_used', 'query_cache', ['last_used_at'])
    
    # Create apr_data table
    op.create_table(
        'apr_data',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('pool_id', sa.String(100), nullable=False, unique=True),
        sa.Column('pool_name', sa.String(200), nullable=True),
        sa.Column('apr_value', sa.Float(), nullable=False),
        sa.Column('apy_value', sa.Float(), nullable=True),
        sa.Column('tvl', sa.Float(), nullable=True),
        sa.Column('metadata', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )
    
    op.create_index('idx_apr_data_pool_id', 'apr_data', ['pool_id'])
    op.create_index('idx_apr_data_updated_at', 'apr_data', ['updated_at'])
    
    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('session_data', JSONB, nullable=True),
        sa.Column('query_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_query', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('last_activity_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )
    
    op.create_index('idx_sessions_last_activity', 'sessions', ['last_activity_at'])
    
    # Create query_logs table
    op.create_table(
        'query_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('session_id', UUID(as_uuid=True), nullable=True),
        sa.Column('query_text', sa.Text(), nullable=False),
        sa.Column('query_type', sa.String(50), nullable=True),
        sa.Column('response_time_ms', sa.Integer(), nullable=False),
        sa.Column('was_cached', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('llm_provider', sa.String(50), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('api_key_hash', sa.String(64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )
    
    op.create_index('idx_query_logs_created_at', 'query_logs', ['created_at'])
    op.create_index('idx_query_logs_session_id', 'query_logs', ['session_id'])
    op.create_index('idx_query_logs_query_type', 'query_logs', ['query_type'])


def downgrade() -> None:
    op.drop_table('query_logs')
    op.drop_table('sessions')
    op.drop_table('apr_data')
    op.drop_table('query_cache')
    op.drop_table('documents')
    
    op.execute('DROP EXTENSION IF EXISTS vector')
