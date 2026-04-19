# TODO 1: Create configuration class
# - Load FOUNDRY_API_KEY from environment
# - Set chunk_size, chunk_overlap, k (number of chunks to retrieve)
# - Set embedding model name, LLM model name, temperature
# - Use pydantic-settings or python-dotenv
"""Configuration module for RAG Playground application."""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    FOUNDRY_API_KEY: str = os.getenv("FOUNDRY_API_KEY", "")
    FOUNDRY_ENDPOINT: str = os.getenv("FOUNDRY_ENDPOINT", "https://api.foundry.ai/v1")

    # RAG Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    K: int = 3  # Number of chunks to retrieve

    # Model Configuration
    EMBEDDING_MODEL: str = "text-embedding-3-large"
    LLM_MODEL: str = "gpt-5.4-mini"
    TEMPERATURE: float = 0.0

    # Chroma Vector Store
    CHROMA_DB_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "rag_collection"


settings = Settings()
