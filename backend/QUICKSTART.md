# ⚡ Quick Start Guide

Get Chewie AI Backend running in 2 minutes.

## 🚀 One-Command Setup

```bash
# Clone, configure, and start
git clone <repo-url> && cd c_ai_backend
cp .env.example .env
docker-compose up -d

# Wait 30 seconds for migrations to complete
sleep 30

# Test the API
curl http://localhost:8005/health
```

## ✅ Verify Installation

**1. Check all services are running:**
```bash
docker-compose ps
# Should show: chewie_api, chewie_postgres, chewie_redis (all healthy)
```

**2. Open test UI:**
```
http://localhost:8005/test_api.html
```

**3. Try a query:**
- Select protocol: **Kamino Finance**
- Query: "What is Kamino Finance?"
- Click **Send Request**

## 🎯 What's Running

| Service | URL | Purpose |
|---------|-----|---------|
| API | http://localhost:8005 | Main API server |
| Docs | http://localhost:8005/docs | Interactive API docs |
| Test UI | http://localhost:8005/test_api.html | Test interface |
| PostgreSQL | localhost:5476 | Database |
| Redis | localhost:6385 | Cache |

## 🔑 Default Configuration

The `.env` file uses **mock LLM** by default (no API keys needed).

**To use real LLM:**
```bash
# Edit .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

## 📝 Common Commands

```bash
# View logs
docker logs chewie_api -f

# Restart API
docker-compose restart api

# Stop all
docker-compose down

# Full reset (deletes data!)
docker-compose down -v
docker-compose up -d
```

## 🌐 Supported Protocols

**Solana (Primary):**
Kamino, Marinade, Raydium, Orca, Jupiter, Drift, Mango, Reflect

## 🆘 Troubleshooting

**API not responding?**
```bash
docker logs chewie_api --tail 20
```

**Port already in use?**
Edit `.env`:
```bash
POSTGRES_EXTERNAL_PORT=5477  # Change from 5476
REDIS_EXTERNAL_PORT=6386     # Change from 6385
API_EXTERNAL_PORT=8006       # Change from 8005
```

**Database connection error?**
```bash
# Check PostgreSQL is healthy
docker logs chewie_postgres
```

