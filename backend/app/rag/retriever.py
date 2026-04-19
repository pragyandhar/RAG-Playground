# TODO 7: Implement retrieval logic
# Function: retrieve(query: str, retriever: Retriever) -> List[Document]
# - Just a wrapper around retriever.invoke()
# - Add logging for debugging
# (Keep separate file for future RAG types where retrieval is complex)

import logging
from typing import List
from langchain_core.documents import Document

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def retrieve(query: str, retriever) -> List[Document]:
    """Retrieve relevant documents for a query using the given retriever.

    Args:
        query: The search query string
        retriever: A LangChain retriever instance (e.g., Chroma.as_retriever())

    Returns:
        List of relevant Document objects

    Raises:
        ValueError: If query is empty or retriever is invalid
        RuntimeError: If retrieval fails
    """
    # Input validation
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")

    if not hasattr(retriever, "invoke"):
        raise ValueError("Retriever must have an 'invoke' method")

    try:
        logger.info(f"Retrieving documents for query: '{query[:50]}...'")

        # Invoke retriever - returns List[Document]
        results = retriever.invoke(query)

        logger.info(f"Retrieved {len(results)} documents")

        return results

    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        raise RuntimeError(f"Failed to retrieve documents: {e}")