"""Add dapp and client_id fields to tables

Revision ID: add_dapp_client_id
Revises: initial_schema
Create Date: 2025-10-29 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_dapp_client_id'
down_revision: Union[str, None] = 'initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add dapp and client_id to query_cache
    op.add_column('query_cache', sa.Column('dapp', sa.String(100), nullable=False, server_default='kamino'))
    op.add_column('query_cache', sa.Column('client_id', sa.String(255), nullable=True))
    
    # Create indexes for query_cache
    op.create_index('idx_query_cache_dapp', 'query_cache', ['dapp'])
    op.create_index('idx_query_cache_client_id', 'query_cache', ['client_id'])
    
    # Add dapp to apr_data and modify unique constraint
    # First, drop the old unique constraint on pool_id
    op.drop_constraint('apr_data_pool_id_key', 'apr_data', type_='unique')
    
    # Add dapp column
    op.add_column('apr_data', sa.Column('dapp', sa.String(100), nullable=False, server_default='kamino'))
    
    # Create new composite unique index
    op.create_index('idx_apr_data_dapp_pool', 'apr_data', ['dapp', 'pool_id'], unique=True)
    op.create_index('idx_apr_data_dapp', 'apr_data', ['dapp'])
    
    # Add client_id and dapp to sessions
    op.add_column('sessions', sa.Column('client_id', sa.String(255), nullable=True))
    op.add_column('sessions', sa.Column('dapp', sa.String(100), nullable=False, server_default='kamino'))
    
    # Create indexes for sessions
    op.create_index('idx_sessions_client_id', 'sessions', ['client_id'])
    op.create_index('idx_sessions_dapp', 'sessions', ['dapp'])
    
    # Add client_id and dapp to query_logs
    op.add_column('query_logs', sa.Column('client_id', sa.String(255), nullable=True))
    op.add_column('query_logs', sa.Column('dapp', sa.String(100), nullable=False, server_default='kamino'))
    
    # Create indexes for query_logs
    op.create_index('idx_query_logs_client_id', 'query_logs', ['client_id'])
    op.create_index('idx_query_logs_dapp', 'query_logs', ['dapp'])


def downgrade() -> None:
    # Remove indexes and columns from query_logs
    op.drop_index('idx_query_logs_dapp', 'query_logs')
    op.drop_index('idx_query_logs_client_id', 'query_logs')
    op.drop_column('query_logs', 'dapp')
    op.drop_column('query_logs', 'client_id')
    
    # Remove indexes and columns from sessions
    op.drop_index('idx_sessions_dapp', 'sessions')
    op.drop_index('idx_sessions_client_id', 'sessions')
    op.drop_column('sessions', 'dapp')
    op.drop_column('sessions', 'client_id')
    
    # Remove indexes and columns from apr_data
    op.drop_index('idx_apr_data_dapp', 'apr_data')
    op.drop_index('idx_apr_data_dapp_pool', 'apr_data')
    op.drop_column('apr_data', 'dapp')
    
    # Restore unique constraint on pool_id
    op.create_unique_constraint('apr_data_pool_id_key', 'apr_data', ['pool_id'])
    
    # Remove indexes and columns from query_cache
    op.drop_index('idx_query_cache_client_id', 'query_cache')
    op.drop_index('idx_query_cache_dapp', 'query_cache')
    op.drop_column('query_cache', 'client_id')
    op.drop_column('query_cache', 'dapp')
