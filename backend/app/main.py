# TODO 16: Create FastAPI app
# - Add CORS middleware (allow frontend origin, typically http://localhost:5173)
# - Include router with prefix "/api"
# - Add lifespan event to load vector store into memory

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handler."""
    # Startup: Initialize resources
    from app.rag.embedder import get_embeddings
    from app.rag.vector_store import load_vector_store

    # Initialize embeddings to verify API connection
    get_embeddings()

    # Pre-load vector store if it exists
    load_vector_store()

    yield

    # Shutdown: Cleanup resources (if needed in future)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="RAG Playground API",
        description="Native RAG application with Foundry API integration",
        version="1.0.0",
        lifespan=lifespan,  # Use lifespan instead of deprecated on_event
    )

    # CORS middleware - restrict to frontend origin in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router with prefix
    app.include_router(router, prefix="/api")

    return app


# Create application instance
app = create_app()


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint with API information."""
    return {
        "service": "RAG Playground API",
        "version": "1.0.0",
        "status": "running",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
