#!/bin/bash
# First run setup script

set -e

echo "🚀 Starting Chewie AI Backend first run setup..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys if needed"
fi

# Start containers
echo "🐳 Starting Docker containers..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 15

# Check PostgreSQL is ready
echo "🔍 Checking PostgreSQL status..."
docker-compose exec -T postgres pg_isready -U chewie || {
    echo "❌ PostgreSQL is not ready. Please wait and try again."
    exit 1
}

# Run migrations
echo "🗄️  Running database migrations..."
docker-compose exec -T api alembic upgrade head

# Check health
echo "🏥 Checking API health..."
sleep 5
curl -f http://localhost:8000/health || {
    echo "⚠️  API health check failed. Check logs with: docker-compose logs api"
}

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 Services running:"
echo "  - API: http://localhost:8000"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
echo "🧪 Test the API:"
echo '  curl -X POST http://localhost:8000/ask \'
echo '    -H "X-API-Key: dev-key-123" \'
echo '    -H "Content-Type: application/json" \'
echo '    -d '"'"'{"query": "What is Kamino Finance?"}'"'"
echo ""
echo "📚 Next steps:"
echo "  - Edit .env to add OpenAI/Anthropic API key (optional)"
echo "  - Run scraper: make scrape (optional)"
echo "  - View logs: docker-compose logs -f api"
echo ""
