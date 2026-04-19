# TODO 3: Implement document loading
# Function: load_document(file_path: str) -> List[Document]
# Support: .txt, .pdf (use PyPDFLoader for PDF, TextLoader for TXT)
# Handle file not found, unsupported format

import os
from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader


def load_document(file_path: str) -> List[Document]:
    """Load document with secure path validation - prevents symlinks and directory traversal."""
    # Step 1: Validate inputs - reject empty or None
    if not file_path or not isinstance(file_path, str):
        raise ValueError("Invalid file path: must be a non-empty string")

    # Step 2: Check for symlinks BEFORE resolution (prevents symlink attacks)
    if os.path.islink(file_path):
        raise ValueError("Symlinks are not allowed for security reasons")

    # Step 3: Resolve path strictly - ensures path exists and eliminates symlinks
    try:
        resolved_path = Path(file_path).resolve(strict=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    # Step 4: Validate resolved path is within base directory
    from backend.app.config import settings
    base_dir = Path(settings.CHROMA_DB_PATH).parent / "documents"
    base_dir.mkdir(parents=True, exist_ok=True)

    try:
        resolved_path.relative_to(base_dir)
    except ValueError:
        raise ValueError(f"Access denied: file outside allowed directory")

    # Step 5: Allowlist - only allow specific file extensions
    allowed_extensions = {".txt", ".pdf"}
    if resolved_path.suffix.lower() not in allowed_extensions:
        raise ValueError(f"File extension not allowed: {resolved_path.suffix}")

    # Step 6: Double-check no traversal occurred (ensure no .. in original or resolved)
    if ".." in str(resolved_path):
        raise ValueError("Invalid file path: directory traversal detected")

    # Step 7: Load document based on type
    try:
        if resolved_path.suffix.lower() == ".txt":
            loader = TextLoader(str(resolved_path), encoding="utf-8")
        else:  # .pdf
            loader = PyPDFLoader(str(resolved_path))

        return loader.load()
    except Exception as e:
        raise RuntimeError(f"Failed to load document: {e}")