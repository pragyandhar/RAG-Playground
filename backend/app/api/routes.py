# TODO 9: Import all rag modules
# TODO 10: POST /ingest endpoint
# - Accept file upload (UploadFile)
# - Save temporarily
# - Call load_document -> split_documents -> create_vector_store
# - Return IngestResponse with num_chunks

# TODO 11: POST /query endpoint
# - Accept QueryRequest
# - Load vector store (if not exists, return error)
# - Get retriever, run chain
# - Return QueryResponse with answer + sources

# TODO 12: GET /health endpoint
# - Return {"status": "ok"}
# =================================================================
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List
import os

from app.models import QueryRequest, QueryResponse, IngestResponse, SourceDocument
from app.rag.loader import load_document
from app.rag.splitter import split_documents
from app.rag.vector_store import create_vector_store, load_vector_store, get_retriever
from app.rag.embedder import get_embeddings
from app.rag.chain import create_rag_chain
from app.rag.retriever import retrieve

router = APIRouter()


def get_llm():
    """Get LLM instance from config."""
    from langchain_openai import ChatOpenAI
    from app.config import settings
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.TEMPERATURE,
        openai_api_key=settings.FOUNDRY_API_KEY,
        openai_api_base=settings.FOUNDRY_ENDPOINT,
    )


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    """Ingest a document and create vector store.

    Args:
        file: PDF or TXT file to ingest

    Returns:
        IngestResponse with number of chunks created
    """
    # Input validation
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    ext = Path(file.filename).suffix.lower()
    if ext not in [".txt", ".pdf"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {ext}")

    # Validate file size (max 10MB)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset
    max_size = 10 * 1024 * 1024  # 10MB
    if file_size > max_size:
        raise HTTPException(status_code=400, detail=f"File too large: {file_size} bytes")

    # Save temporarily and process
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / file.filename
        content = await file.read()
        temp_path.write_bytes(content)

        try:
            # Load document
            documents = load_document(str(temp_path))

            # Split into chunks
            chunks = split_documents(documents)

            # Create vector store
            vector_store = create_vector_store(chunks)

            # Get retriever and retrieve to confirm
            retriever = get_retriever(vector_store)
            # Test retrieval to ensure setup works
            _ = retrieve("test", retriever)

            return IngestResponse(
                message=f"Successfully ingested {file.filename}",
                num_chunks=len(chunks),
                persisted_path="chroma_db",  # Persistence path from config
            )
        finally:
            # Cleanup temp file
            if temp_path.exists():
                temp_path.unlink()

    raise HTTPException(status_code=500, detail="Ingestion failed")


@router.post("/query", response_model=QueryResponse)
async def query(query_req: QueryRequest):
    """Query the document store.

    Args:
        query_req: QueryRequest with question

    Returns:
        QueryResponse with answer and sources
    """
    if not query_req.question or not query_req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Load vector store
    vector_store = load_vector_store()
    if vector_store is None:
        raise HTTPException(
            status_code=400,
            detail="Vector store not found. Please ingest a document first."
        )

    try:
        # Get chain and run
        retriever = get_retriever(vector_store)
        llm = get_llm()
        chain = create_rag_chain(retriever, llm)

        # Run chain
        result = chain.invoke({"input": query_req.question})

        # Get sources from retrieval
        retrieved_docs = retrieve(query_req.question, retriever)
        sources = [
            SourceDocument(
                content=doc.page_content,
                metadata=doc.metadata or {}
            )
            for doc in retrieved_docs
        ]

        return QueryResponse(
            answer=result["answer"],
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}