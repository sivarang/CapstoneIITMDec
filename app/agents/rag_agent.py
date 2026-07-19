"""
RAG Agent

Retrieves relevant documentation from Pinecone.
"""

from langchain_core.messages import HumanMessage

from app.rag.retriever import retrieve_documents

from app.utils.logger import (
    log_agent_start,
    log_agent_end,
    log_rag,
    log_docs,
    log_error,
)


def rag_agent(state):

    log_agent_start("RAG Agent")

    #
    # Retrieve the latest user message
    #
    human_messages = [
    m.content
    for m in state["messages"]
    if isinstance(m, HumanMessage)
]

    question = "\n".join(human_messages[-1:])
    print("=" * 50)
    print("RAG QUERY")
    print(f"Router : {state.get('router_vendor')} {state.get('router_model')}")
    print(f"Question: {question}")
    print("=" * 50)

    #
    # Retrieve documents
    #
    search_query = f"""
Router Make: {state.get('router_vendor')}
Router Model: {state.get('router_model')}

User Message:
{question}
"""
    print(search_query)
    docs = retrieve_documents(
    query=search_query,
    router_model=state.get("router_model", "")
    )

    #
    # Nothing found
    #
    if not docs:

        state["manual_found"] = False
        state["retrieved_context"] = ""

        state["next_action"] = "TROUBLESHOOT"

        log_rag("No documents found.")
        log_agent_end("RAG Agent")

        return state

    #
    # Build retrieved context
    #
    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    state["manual_found"] = True
    state["retrieved_context"] = context

    #
    # Optional logging
    #
    print("=" * 50)
    print("Retrieved Context")
    print(context[:800])      # print first 800 chars
    print("=" * 50)

    log_docs(docs)
    log_rag(f"Retrieved {len(docs)} document(s).")

    #
    # Continue to Troubleshooter
    #
    state["next_action"] = "TROUBLESHOOT"

    log_agent_end("RAG Agent")

    return state