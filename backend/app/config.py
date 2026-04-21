from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    # LLM API
    GROQ_API_KEY: str
    
    # Embeddings API
    GOOGLE_API_KEY: str

    # Vector Database
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = "*"

    # LangSmith (Optional)
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "agentic-support-system"
    LANGCHAIN_ENDPOINT: str = ""

    # Vector DB Collection
    COLLECTION_NAME: str = "support_docs"


settings = Settings()
