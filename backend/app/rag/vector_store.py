# TODO 6: Implement vector store operations
# Function: create_vector_store(chunks: List[Document]) -> Chroma
# - Use Chroma.from_documents()
# - Persist to directory from config
#
# Function: load_vector_store() -> Chroma
# - Load existing store from disk
# - Return None if doesn't exist
#
# Function: get_retriever(vector_store: Chroma) -> Retriever
# - Use .as_retriever() with k from config

from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_chroma import Chroma

from ..config import settings
from .embedder import get_embeddings


class VectorStoreManager:
    """Manager for Chroma vector store operations."""

    _instance: Optional["VectorStoreManager"] = None

    def __new__(cls):
        """Singleton pattern - ensure single instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize vector store manager."""
        if not hasattr(self, "_initialized"):
            self._db_path = Path(settings.CHROMA_DB_PATH)
            self._collection_name = settings.COLLECTION_NAME
            self._retriever_k = settings.K
            self._initialized = True

    def _ensure_db_directory(self) -> Path:
        """Ensure database directory exists with proper permissions."""
        self._db_path.mkdir(parents=True, exist_ok=True)
        return self._db_path

    def create_vector_store(self, chunks: List[Document]) -> Chroma:
        """Create new vector store from document chunks."""
        if not chunks:
            raise ValueError("Cannot create vector store with empty chunks")

        self._ensure_db_directory()

        embeddings = get_embeddings()

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(self._db_path),
            collection_name=self._collection_name,
        )
        vector_store.persist()

        return vector_store

    def load_vector_store(self) -> Optional[Chroma]:
        """Load existing vector store from disk. Returns None if not found."""
        if not self._db_path.exists():
            return None

        try:
            embeddings = get_embeddings()
            return Chroma(
                persist_directory=str(self._db_path),
                embedding_function=embeddings,
                collection_name=self._collection_name,
            )
        except Exception:
            return None

    def get_retriever(self, vector_store: Chroma):
        """Get retriever with configurable k value."""
        return vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self._retriever_k},
        )


# Module-level convenience functions
def create_vector_store(chunks: List[Document]):
    """Create vector store from chunks."""
    manager = VectorStoreManager()
    return manager.create_vector_store(chunks)


def load_vector_store():
    """Load existing vector store."""
    manager = VectorStoreManager()
    return manager.load_vector_store()


def get_retriever(vector_store):
    """Get retriever for vector store."""
    manager = VectorStoreManager()
    return manager.get_retriever(vector_store)
