# TODO 5: Create embedding function
# Function: get_embeddings() -> OpenAIEmbeddings
# Initialize with model from config
# Singleton pattern (reuse across requests)

from typing import Optional
from langchain_openai import OpenAIEmbeddings

from ..config import settings


class EmbeddingManager:
    """Singleton manager for OpenAI embeddings with caching and validation."""

    _instance: Optional[OpenAIEmbeddings] = None

    def __new__(cls):
        """Ensure singleton instance."""
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize embedding client once."""
        if not hasattr(self, "_client"):
            self._client = self._create_client()

    def _create_client(self) -> OpenAIEmbeddings:
        """Create embeddings client with config validation."""
        if not settings.FOUNDRY_API_KEY:
            raise ValueError("FOUNDRY_API_KEY environment variable is not set")

        # Configure client - use Foundry endpoint with OpenAI-compatible interface
        client = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.FOUNDRY_API_KEY,
            openai_api_base=settings.FOUNDRY_ENDPOINT,
            openai_headers={
                "User-Agent": "RAG-Playground/1.0",
            },
        )
        return client

    def get_embeddings(self) -> OpenAIEmbeddings:
        """Get singleton embedding client instance."""
        return self._client


# Module-level convenience function
def get_embeddings() -> OpenAIEmbeddings:
    """Get the singleton embeddings instance."""
    manager = EmbeddingManager()
    return manager.get_embeddings()


