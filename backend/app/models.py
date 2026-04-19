from pydantic import BaseModel
from typing import List, Optional

# TODO 2: Create these Pydantic models:
class IngestRequest(BaseModel):
    """Request model for document ingestion."""

    file_path: str


class IngestResponse(BaseModel):
    """Response model for document ingestion."""

    message: str
    num_chunks: int
    persisted_path: str


class QueryRequest(BaseModel):
    """Request model for querying documents."""

    question: str
    k: Optional[int] = None  # Override default k if provided


class SourceDocument(BaseModel):
    """Model for source document metadata."""

    content: str
    metadata: dict


class QueryResponse(BaseModel):
    """Response model for query results."""

    answer: str
    sources: List[SourceDocument]