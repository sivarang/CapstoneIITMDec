"""
Retriever
"""

from app.rag.vectorstore import get_retriever

from app.utils.logger import (
    logger,
    log_error,
)
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from app.config import PINECONE_INDEX_NAME

embeddings = OpenAIEmbeddings()

vectorstore = PineconeVectorStore(
    index_name=PINECONE_INDEX_NAME,
    embedding=embeddings,
)

ROUTER_NAMESPACE = {
    "Archer C5": "tp-link-archer-c5",
    "D7000": "netgear-d7000",
}

def retrieve_documents(
    query: str,
    router_model: str = ""
):

    try:

        namespace = ROUTER_NAMESPACE.get(router_model)

        print("RAG QUERY BEING SENT")
        print(query)
        docs = vectorstore.similarity_search(
        query=query,
        k=5,
        namespace=namespace,
        )

        logger.info(
            f"Pinecone returned {len(docs)} document(s)"
        )

        return docs

    except Exception as e:

        log_error(e)

        return []