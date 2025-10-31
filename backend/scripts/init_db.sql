-- Initialize PostgreSQL database with pgvector extension

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom functions for vector operations
CREATE OR REPLACE FUNCTION cosine_distance(a vector, b vector)
RETURNS float
AS $$
    SELECT 1 - (a <=> b);
$$ LANGUAGE SQL IMMUTABLE STRICT PARALLEL SAFE;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE chewie_ai TO chewie;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO chewie;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO chewie;

-- Create indexes will be handled by Alembic migrations
