import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    google_api_key: Optional[str] = None
    langsmith_api_key: Optional[str] = None
    
    # LangSmith Configuration
    langsmith_tracing: bool = True
    
    # LLM Configuration
    model_name: str = "gemini-2.5-flash"
    
    # API Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Legacy support
    @property
    def api_host(self) -> str:
        return self.host
    
    @property
    def api_port(self) -> int:
        return self.port
    
    cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env file


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


def setup_environment():
    """Setup environment variables for LangSmith."""
    settings = get_settings()
    
    if settings.google_api_key:
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key
    
    if settings.langsmith_api_key:
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
        os.environ["LANGSMITH_TRACING"] = str(settings.langsmith_tracing).lower()
