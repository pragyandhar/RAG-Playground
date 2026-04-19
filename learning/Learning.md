### How is security handled in this project.
/backend/app/rag/loader.py
Security:
- Directory Traversal Prevention (For more go to DTP.md)
- Files must be within documents/ subdirectory of ChromaDB path
- Validated File Extensions only (.txt and .pdf)

### How is scalability handled in this project
/backend/app/rag/loader.py
- Uses Path for cross-platform compatibility, configurable allowed directory