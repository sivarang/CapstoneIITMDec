"""
Centralized Pinecone Vector Store

Used by:
- ingest.py
- retriever.py
"""

from pinecone import Pinecone

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from app.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
)

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def get_vectorstore() -> PineconeVectorStore:
    """
    Return a Pinecone Vector Store instance.
    """

    return PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
    )


def get_retriever(
    router_model: str | None = None,
    k: int = 3,
):
    """
    Return a retriever.

    If router_model is supplied,
    search only within that manual.
    """

    vectorstore = get_vectorstore()

    search_kwargs = {"k": k}

    if router_model:

        search_kwargs["filter"] = {
            "router_model": router_model
        }

    return vectorstore.as_retriever(
        search_kwargs=search_kwargs
    )