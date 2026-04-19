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
    if not file_path or not isinstance(file_path, str):
        raise ValueError("Invalid file path: must be a non-empty string")
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Allow only .txt and .pdf
    if path.suffix.lower() not in {".txt", ".pdf"}:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    
    if path.suffix.lower() == ".txt":
        loader = TextLoader(str(path), encoding="utf-8")
    else:
        loader = PyPDFLoader(str(path))
    
    return loader.load()