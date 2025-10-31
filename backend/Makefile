.PHONY: help dev docker-up docker-down docker-logs test lint format clean migrate scrape

help:
	@echo "Available commands:"
	@echo "  make dev          - Run locally (without Docker)"
	@echo "  make docker-up    - Start Docker containers (dev mode)"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make docker-logs  - View Docker logs"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make migrate      - Run database migrations"
	@echo "  make scrape       - Run GitBook scraper"
	@echo "  make clean        - Clean cache and temp files"

dev:
	@echo "Starting local development server..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-up:
	@echo "Starting Docker containers (dev mode)..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"
	@echo "Traefik: http://localhost:8080"

docker-down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

docker-logs:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f api

test:
	pytest tests/ -v --cov=app --cov-report=html

lint:
	ruff check app/
	mypy app/

format:
	ruff format app/
	isort app/

migrate:
	alembic upgrade head

scrape:
	python -m app.cli.scraper --source kamino

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/
