"""Tests for /ask endpoint."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ask_endpoint_without_api_key(client: AsyncClient):
    """Test that endpoint requires API key."""
    response = await client.post("/ask", json={
        "query": "What is Kamino Finance?"
    })
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_ask_endpoint_with_invalid_api_key(client: AsyncClient):
    """Test with invalid API key."""
    response = await client.post(
        "/ask",
        json={"query": "What is Kamino Finance?"},
        headers={"X-API-Key": "invalid-key"}
    )
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_ask_endpoint_basic_query(client: AsyncClient):
    """Test basic query with valid API key."""
    response = await client.post(
        "/ask",
        json={
            "query": "What is Kamino Finance?",
            "context": {"dapp": "kamino", "lang": "en"}
        },
        headers={"X-API-Key": "dev-key-123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "answer" in data
    assert "session_id" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0


@pytest.mark.asyncio
async def test_ask_endpoint_earnings_query(client: AsyncClient):
    """Test earnings query."""
    response = await client.post(
        "/ask",
        json={
            "query": "How much can I earn on 1000 USDC?",
            "pool_id": "allez-usdc",
            "amount": 1000,
            "currency": "USDC",
            "context": {"dapp": "kamino", "lang": "en"}
        },
        headers={"X-API-Key": "dev-key-123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "answer" in data
    assert "earnings" in data
    assert "assumptions" in data
    
    if data["earnings"]:
        assert "yearly" in data["earnings"]
        assert "monthly" in data["earnings"]
        assert "apr_value" in data["earnings"]


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] in ["healthy", "degraded"]
    assert "timestamp" in data
