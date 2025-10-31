"""
Main /ask endpoint for handling user queries.
"""

import time
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_api_key
from app.core.config import get_settings
from app.models.schemas import AskRequest, AskResponse, EarningsData, Source, QueryAssumptions
from app.services.llm_service import get_llm_service
from app.services.rag_service import get_rag_service
from app.services.kamino_service import get_kamino_service
from app.services.earnings_calculator import get_earnings_calculator
from app.services.query_classifier import get_query_classifier
from app.services.cache_service import get_cache_service

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key),
) -> AskResponse:
    """
    Main endpoint for asking questions about Kamino Finance.
    
    Workflow:
    1. Classify query type (earnings, general, risk, etc.)
    2. Check cache for similar queries
    3. If earnings query, fetch APR data
    4. Retrieve relevant documents (RAG)
    5. Generate answer with LLM
    6. Cache response
    7. Return formatted response
    """
    start_time = time.time()
    
    # Initialize services
    llm_service = get_llm_service()
    rag_service = get_rag_service()
    kamino_service = get_kamino_service()
    calculator = get_earnings_calculator()
    classifier = get_query_classifier()
    cache_service = get_cache_service()
    
    # Extract context
    dapp = request.context.dapp if request.context else "kamino"
    client_id = request.client_id or "unknown"
    session_id = str(uuid.uuid4())
    
    # Check if query mentions other protocols (early refusal)
    other_protocols = [
        "aave", "compound", "uniswap", "curve", "convex", "yearn", "maker", "lido",
        "hyperliquid", "dydx", "gmx", "synthetix", "balancer", "sushiswap",
        "pancakeswap", "trader joe", "benqi"
    ]
    query_lower = request.query.lower()
    current_protocol = dapp.lower()
    
    # Check if query mentions a different protocol
    mentioned_protocol = None
    for protocol in other_protocols:
        if protocol in query_lower and protocol != current_protocol:
            mentioned_protocol = protocol
            break
    
    # If asking about a different protocol, return refusal immediately
    if mentioned_protocol:
        protocol_names = {
            "kamino": "Kamino Finance",
            "marinade": "Marinade Finance",
            "raydium": "Raydium",
            "orca": "Orca",
            "jupiter": "Jupiter",
            "drift": "Drift Protocol",
            "mango": "Mango Markets",
            "reflect": "Reflect"
        }
        current_name = protocol_names.get(current_protocol, f"{current_protocol} DeFi")
        
        return AskResponse(
            answer=f"I can only answer questions about {current_name}, as I'm the assistant widget on their page. For information about other protocols, please visit their official website.",
            earnings=None,
            assumptions=None,
            confidence=1.0,
            sources=None,
            followups=None,
            session_id=session_id,
            dapp=dapp
        )
    
    # Use provided session ID if available
    session_id = request.session_id or session_id
    
    # Step 1: Classify query
    classification = classifier.classify(
        request.query,
        pool_id=request.pool_id
    )
    
    query_type = classification["query_type"]
    pool_id = classification["pool_id"] or request.pool_id
    amount = classification["amount"] or request.amount
    currency = classification["currency"] or request.currency
    
    # Step 2: Check cache (Redis first for exact match, then PostgreSQL for semantic)
    settings = get_settings()
    cached_response = await cache_service.get_from_redis(request.query, dapp=dapp)
    if not cached_response:
        cached_response = await cache_service.get_cached_response(
            request.query,
            db,
            dapp=dapp,
            similarity_threshold=0.95,
            max_age_seconds=settings.cache_ttl_seconds,
        )
    
    if cached_response:
        # Return cached response with updated session_id
        cached_response["session_id"] = session_id
        return AskResponse(**cached_response)
    
    # Step 3: Handle earnings queries
    earnings_data = None
    assumptions = None
    apr_data = None
    
    if query_type == "earnings" and pool_id:
        # Fetch APR data
        apr_data = await kamino_service.get_pool_apr(pool_id)
        
        if apr_data:
            # Calculate earnings
            earnings = calculator.calculate_earnings(
                amount=amount,
                apr=apr_data["apr"],
                currency=currency
            )
            
            earnings_data = EarningsData(
                yearly=earnings["yearly"],
                monthly=earnings["monthly"],
                apr_value=apr_data["apr"],
                updated_at=kamino_service.format_time_ago(apr_data["updated_at"])
            )
            
            assumptions = QueryAssumptions(
                pool=pool_id,
                amount=amount,
                currency=currency
            )
    
    # Step 4: Retrieve relevant documents (RAG)
    relevant_docs = await rag_service.retrieve_relevant_documents(
        query=request.query,
        db=db,
        top_k=3,
        similarity_threshold=0.7,
        dapp=dapp
    )
    
    context = await rag_service.build_context(relevant_docs, max_length=2000)
    
    # Step 5: Generate answer with LLM
    llm_response = await llm_service.generate_answer(
        query=request.query,
        context=context,
        query_type=query_type,
        dapp=dapp,
        temperature=0.7,
    )
    
    answer_text = llm_response["content"]
    
    # If earnings query, enhance answer with calculated data
    if earnings_data:
        answer_prefix = (
            f"Based on current rates, depositing {calculator.format_currency(amount, currency)} "
            f"into the {apr_data['pool_name']} pool can earn you approximately "
            f"{calculator.format_currency(earnings_data.yearly)} per year "
            f"({calculator.format_currency(earnings_data.monthly)} per month).\n\n"
        )
        answer_text = answer_prefix + answer_text
    
    # Step 6: Generate sources
    sources = []
    if apr_data and pool_id:
        sources.append(Source(
            title=f"Kamino {apr_data['pool_name']} Pool",
            url=f"https://kamino.finance/lend/{pool_id}"
        ))
    
    for doc in relevant_docs[:2]:  # Top 2 sources
        sources.append(Source(
            title=doc["title"],
            url=doc["url"]
        ))
    
    # Step 7: Generate follow-up questions (only if not a refusal)
    followups = None
    # Check if answer is a refusal (contains key phrases)
    refusal_phrases = [
        "I can only answer questions about",
        "I'm a DeFi assistant",
        "can only help with",
        "Please ask me about DeFi",
        "visit their official website"
    ]
    is_refusal = any(phrase in answer_text for phrase in refusal_phrases)
    
    if not is_refusal:
        followups = await llm_service.generate_followup_questions(
            query=request.query,
            answer=answer_text,
            count=3
        )
    
    # Calculate confidence
    confidence = classification.get("confidence", 0.7)
    if relevant_docs:
        # Boost confidence if we have good context
        avg_similarity = sum(doc["similarity"] for doc in relevant_docs) / len(relevant_docs)
        confidence = min((confidence + avg_similarity) / 2, 1.0)
    
    # Build response
    response = AskResponse(
        answer=answer_text,
        earnings=earnings_data,
        assumptions=assumptions,
        confidence=round(confidence, 2),
        sources=sources if sources else None,
        followups=followups if followups else None,
        session_id=session_id,
        dapp=dapp
    )
    
    # Step 8: Cache response
    await cache_service.save_response(
        query=request.query,
        response=response,
        db=db,
        dapp=dapp,
        query_type=query_type,
        pool_id=pool_id,
        amount=amount,
        currency=currency,
        client_id=client_id,
        llm_provider=llm_response.get("provider", "openai"),
        llm_model=llm_response.get("model", "gpt-4"),
        confidence=confidence,
    )
    
    # Log query (for analytics)
    response_time = int((time.time() - start_time) * 1000)
    # TODO: Add to QueryLog table
    
    return response


@router.get("/ask/test")
async def test_ask_endpoint():
    """Test endpoint to verify API is working."""
    return {
        "status": "ok",
        "message": "Ask endpoint is operational",
        "endpoints": {
            "POST /ask": "Main query endpoint"
        }
    }
