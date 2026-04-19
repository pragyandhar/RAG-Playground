# TODO 8: Create the RAG chain
# Function: create_rag_chain(retriever, llm) -> Chain
# Steps:
# 1. Create ChatPromptTemplate with system message:
#    "Answer using ONLY context. If not in context, say 'I don't know'"
# 2. Create stuff documents chain using create_stuff_documents_chain
# 3. Create retrieval chain using create_retrieval_chain
# 4. Return the chain

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.retrievers import BaseRetriever
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain


def create_rag_chain(retriever: BaseRetriever, llm: BaseLanguageModel):
    """Create a RAG chain for question-answering.

    Args:
        retriever: LangChain retriever instance for fetching documents
        llm: Language model for generating answers

    Returns:
        A runnable RAG chain that accepts input with 'input' key

    Raises:
        ValueError: If retriever or llm is invalid
    """
    # Input validation
    if not hasattr(retriever, "invoke"):
        raise ValueError("Retriever must have an 'invoke' method")

    if not hasattr(llm, "invoke") and not hasattr(llm, "generate"):
        raise ValueError("LLM must have 'invoke' or 'generate' method")

    # System prompt enforces answer-only-from-context behavior
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following context to answer the question. "
        "If the answer is not in the context, say 'I don't know'. "
        "Do not generate fictional information.\n\n"
        "{context}"
    )

    # Step 1: Create prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # Step 2: Create stuff documents chain
    document_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt,
        document_variable_name="context",
    )

    # Step 3: Create retrieval chain
    retrieval_chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=document_chain,
    )

    return retrieval_chain