# 🤖 Chewie AI Backend

**AI-powered DeFi assistant for Solana ecosystem** with RAG, multi-protocol support, and intelligent caching.

## ✨ Features

- 🔮 **Multi-LLM Support** - OpenAI, Anthropic, or local models
- 🧠 **RAG with pgvector** - Semantic search over protocol documentation
- 🕷️ **Documentation Scraper** - Index GitBook docs automatically
- 💰 **Real-time APR Data** - Live yield data from Solana protocols
- 🎯 **Smart Query Classification** - Earnings, risk, general queries
- ⚡ **Intelligent Caching** - Redis + semantic similarity matching
- 🔐 **Multi-Protocol** - 8 Solana protocols supported
- 📊 **Analytics** - Track usage by protocol and client
- 🎯 **Protocol-Specific Responses** - Only answers about the active protocol (browser extension mode)

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repo-url> && cd c_ai_backend
cp .env.example .env

# Start services (auto-runs migrations)
docker-compose up -d

# Check status
docker-compose ps
docker logs chewie_api
```

**Access:**
- API: http://localhost:8005
- Docs: http://localhost:8005/docs
- Test UI: http://localhost:8005/test_api.html

**Production (with HTTPS):**
```bash
# Set in .env: TRAEFIK_ENABLE=true, API_DOMAIN=api.yourdomain.com
docker-compose --profile production up -d
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 🌐 Supported Solana Protocols

- **Kamino Finance** - Lending & Liquidity (full integration with real-time APR)
- **Marinade** - Liquid Staking
- **Raydium** - DEX & AMM
- **Orca** - DEX & Concentrated Liquidity
- **Jupiter** - Swap Aggregator
- **Drift** - Perpetuals Trading
- **Mango Markets** - Trading Platform
- **Reflect** - Autonomous Money

See [ADDING_NEW_PROTOCOL.md](docs/ADDING_NEW_PROTOCOL.md) to add more Solana protocols.

## 🔑 API Usage

**POST /api/v1/ask** - Main endpoint for DeFi queries

```bash
curl -X POST http://localhost:8005/api/v1/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key-123" \
  -d '{
    "query": "How much can I earn on 1000 USDC in Kamino?",
    "pool_id": "USDC",
    "amount": 1000,
    "currency": "USDC",
    "context": {"dapp": "kamino", "lang": "en"},
    "client_id": "my-app-v1"
  }'
```

**Response:**
```json
{
  "answer": "Based on current rates, depositing 1,000 USDC...",
  "earnings": {"yearly": 124.0, "monthly": 10.33, "apr_value": 0.124},
  "confidence": 0.95,
  "sources": [...],
  "followups": ["What are the risks?", ...],
  "session_id": "uuid",
  "dapp": "kamino"
}
```

**Other Endpoints:**
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /admin/cache/stats` - Cache statistics (admin)

## 🔧 Tech Stack

- **Framework:** FastAPI + Uvicorn
- **Database:** PostgreSQL 16 + pgvector
- **Cache:** Redis 7
- **LLM:** OpenAI / Anthropic / Local models
- **Embeddings:** sentence-transformers
- **Reverse Proxy:** Traefik (production)
- **Deployment:** Docker + Docker Compose

## 📚 Documentation

- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Production deployment guide
- [SCRAPER_GUIDE.md](docs/SCRAPER_GUIDE.md) - Documentation scraper guide
- [ADDING_NEW_PROTOCOL.md](docs/ADDING_NEW_PROTOCOL.md) - Add new DeFi protocols
- [PROTOCOL_RESTRICTION_EXAMPLES.md](docs/PROTOCOL_RESTRICTION_EXAMPLES.md) - Protocol-specific responses
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [EXAMPLES.md](docs/EXAMPLES.md) - API usage examples

## 🔒 Key Features

**Browser Extension Mode:**
- Protocol-specific responses (only answers about the active protocol)
- Context-aware based on `dapp` parameter
- Automatic refusal for cross-protocol questions
- No follow-ups generated for refusal responses

**Security:**
- API key authentication
- CORS protection
- Rate limiting (60 req/min)
- Input validation

**Performance:**
- Redis caching with semantic similarity
- PostgreSQL connection pooling
- Automatic database migrations on startup
- APR data cached for 1 hour

**Monitoring:**
- Health checks at `/health`
- Interactive docs at `/docs`
- Detailed logging

## 📚 Documentation Scraper

Index protocol documentation for RAG (Retrieval-Augmented Generation):

```bash
# Scrape Kamino documentation
docker-compose exec api python -m app.cli.scraper \
  --source kamino \
  --url https://docs.kamino.finance

# Scrape with custom settings
docker-compose exec api python -m app.cli.scraper \
  --source marinade \
  --url https://docs.marinade.finance \
  --max-pages 50 \
  --use-playwright
```

**Features:**
- Scrapes GitBook and similar documentation sites
- Chunks content for optimal RAG performance
- Generates embeddings automatically
- Stores in PostgreSQL with pgvector
- Supports both HTTP client (fast) and Playwright (JS-heavy sites)

**Options:**
- `--source` - Protocol name (kamino, marinade, etc.)
- `--url` - Documentation URL
- `--max-pages` - Maximum pages to scrape (default: 100)
- `--use-playwright` - Use browser automation for JS sites

See [SCRAPER_GUIDE.md](docs/SCRAPER_GUIDE.md) for detailed documentation.

## 🐛 Troubleshooting

```bash
# Check logs
docker logs chewie_api --tail 50

# Check all services
docker-compose ps

# Restart API
docker-compose restart api

# Full reset (deletes data!)
docker-compose down -v && docker-compose up -d
```

## 📝 License

MIT

---

**Built for Solana DeFi** 🌟
