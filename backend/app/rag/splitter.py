# TODO 4: Implement chunking
# Function: split_documents(documents: List[Document]) -> List[Document]
# Use RecursiveCharacterTextSplitter
# Use chunk_size and chunk_overlap from config

from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..config import settings


def split_documents(documents: List[Document]) -> List[Document]:
    """Split documents into chunks with configurable size and overlap."""
    # Validate input
    if not isinstance(documents, list):
        raise TypeError("Documents must be a list of Document objects")

    # Validate each document in the list
    for doc in documents:
        if not isinstance(doc, Document):
            raise TypeError("Each item in documents list must be a Document object")

    # Initialize splitter with config values
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )

    # Split documents - returns List[Document]
    chunks = splitter.split_documents(documents)

    # Validate output
    if not chunks:
        raise ValueError("Document splitting produced no chunks")

    return chunks
