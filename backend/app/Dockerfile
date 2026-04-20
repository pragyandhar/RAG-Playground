FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Use uv lockfile for reproducible dependency installation.
RUN pip install --no-cache-dir uv

# Install project dependencies (without installing the root project package).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy backend application code.
COPY backend/app ./app

# Optionally include existing local data directories.
COPY backend/chroma_db ./chroma_db
COPY backend/documents ./documents

# Keep Chroma persistence at a stable writable path.
ENV CHROMA_DB_PATH=/app/chroma_db

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
