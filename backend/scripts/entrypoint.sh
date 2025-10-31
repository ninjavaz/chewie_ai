#!/bin/bash
set -e

echo "🚀 Starting Chewie AI Backend..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
while ! pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1; do
    sleep 1
done
echo "✅ PostgreSQL is ready!"

# Wait for Redis to be ready (simple sleep approach)
echo "⏳ Waiting for Redis..."
sleep 5
echo "✅ Redis should be ready!"

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head
echo "✅ Migrations completed!"

# Start the application
echo "🎉 Starting Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
