"""
Main FastAPI application for Chewie AI Backend.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.redis import close_redis
from app.api.endpoints import ask, health, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print(f"🚀 Starting {settings.app_name}...")
    print(f"📊 Environment: {settings.app_env}")
    print(f"🤖 LLM Provider: {settings.llm_provider}")
    
    # Initialize database
    await init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    await close_db()
    await close_redis()
    print("✅ Cleanup completed")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered assistant for Kamino Finance with RAG and intelligent caching",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env == "development" else settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


# Trusted host middleware (security)
if settings.app_env == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["api.chewieai.com", "*.chewieai.com"]
    )


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred",
            "type": type(exc).__name__,
        }
    )


# Include routers
app.include_router(
    ask.router,
    tags=["Query"],
)

app.include_router(
    health.router,
    tags=["Health"],
)

app.include_router(
    admin.router,
    tags=["Admin"],
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "status": "operational",
        "environment": settings.app_env,
        "docs": "/docs",
        "endpoints": {
            "POST /ask": "Main query endpoint",
            "GET /health": "Health check",
            "GET /health/detailed": "Detailed health check",
            "GET /admin/cache/stats": "Cache statistics (requires admin key)",
        }
    }


# Metrics endpoint (basic)
@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint."""
    # TODO: Implement proper Prometheus metrics
    return {
        "status": "ok",
        "message": "Metrics endpoint - implement Prometheus integration"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
