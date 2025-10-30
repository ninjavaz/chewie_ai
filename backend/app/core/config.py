from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra env vars (used by docker-compose)
    )
    
    # Application
    app_name: str = Field(default="Chewie AI Backend", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=False, alias="DEBUG")
    api_version: str = Field(default="v1", alias="API_VERSION")
    
    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    # Database
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(default="chewie_ai", alias="POSTGRES_DB")
    postgres_user: str = Field(default="chewie", alias="POSTGRES_USER")
    postgres_password: str = Field(default="change_me", alias="POSTGRES_PASSWORD")
    
    # Redis
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_password: str = Field(default="", alias="REDIS_PASSWORD")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    
    # API Keys (stored as comma-separated string in .env)
    api_keys_str: str = Field(default="dev-key-123", alias="API_KEYS")
    
    @property
    def api_keys(self) -> List[str]:
        """Parse API keys from comma-separated string."""
        return [key.strip() for key in self.api_keys_str.split(',') if key.strip()]
    
    # LLM Configuration
    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    
    # LLM Models
    openai_model: str = Field(default="gpt-4-turbo-preview", alias="OPENAI_MODEL")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20240620", alias="ANTHROPIC_MODEL")
    
    # Embeddings
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL"
    )
    embedding_dimension: int = Field(default=384, alias="EMBEDDING_DIMENSION")
    
    # Cache settings
    cache_ttl_seconds: int = Field(default=30, alias="CACHE_TTL_SECONDS")  # Query cache in seconds
    apr_cache_ttl_seconds: int = Field(default=30, alias="APR_CACHE_TTL_SECONDS")  # APR cache in seconds
    
    # CORS (stored as comma-separated string in .env)
    cors_origins_str: str = Field(
        default="http://localhost:3000",
        alias="CORS_ORIGINS"
    )
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins_str.split(',') if origin.strip()]
    
    # Rate limiting
    rate_limit_per_minute: int = Field(default=60, alias="RATE_LIMIT_PER_MINUTE")
    
    # Kamino API
    kamino_api_url: str = Field(default="https://api.kamino.finance", alias="KAMINO_API_URL")
    kamino_api_key: str = Field(default="mock", alias="KAMINO_API_KEY")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    @property
    def database_url(self) -> str:
        """Construct database URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def redis_url(self) -> str:
        """Construct Redis URL."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance."""
    return settings
