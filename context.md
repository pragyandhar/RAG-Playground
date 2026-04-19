### What am I doing?
I am building a production-grade industry level resume worthy project on native RAG. As I learn about new techniques in RAG, I will apply it in this project only.
My aim is to build modular code and land a high-paying job.
I am building this project to showcase it in my Agentic AI Interviews.

### My Method of Building
I will be using claude code and agentic coding to build this thing.
I have already built my file structure. 
I will write TODOs and provide with the imports. Then Claude Code will build the rest of the stuff STRICTLY based on what I have defined. 
Claude Code can also give me suggestions (if I can add something to make my code scalable and secure. Because this is my first time coding with Claude Code)

### Tech Stack
Backend:
- Langchain
- FastAPI
Frontend:
- React
- Tailwind

### These are the new import locations of Latest Langchain and FastAPI docs
#### Document Loading
from langchain_community.document_loaders import TextLoader, PyPDFLoader

#### Text Splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

#### Embeddings
from langchain_openai import OpenAIEmbeddings

#### Vector Store
from langchain_chroma import Chroma

#### LLM
from langchain_openai import ChatOpenAI

#### Prompts
from langchain_core.prompts import ChatPromptTemplate

#### Chains
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

#### Documents
from langchain_core.documents import Document

#### FastAPI
from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel