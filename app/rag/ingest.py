from pathlib import Path

from pinecone import Pinecone, ServerlessSpec

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings

from langchain_pinecone import PineconeVectorStore


from app.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME
)


# -----------------------------
# Pinecone Initialization
# -----------------------------

pc = Pinecone(
    api_key=PINECONE_API_KEY
)


# -----------------------------
# Create Index if Required
# -----------------------------

existing_indexes = [
    index.name
    for index in pc.list_indexes()
]


if PINECONE_INDEX_NAME not in existing_indexes:

    print(
        f"Creating Pinecone index: {PINECONE_INDEX_NAME}"
    )

    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )


else:

    print(
        f"Index {PINECONE_INDEX_NAME} already exists"
    )

# -----------------------------
# Router Namespace Mapping
# -----------------------------

ROUTER_NAMESPACES = {
    "Archer C5(SP)_UG_V4.pdf": "tp-link-archer-c5",
    "D7000v2_UM_EN.pdf": "netgear-d7000",
}
# -----------------------------
# Load PDF Manuals
# -----------------------------

manual_path = Path(
    "data/manuals"
)


documents = []


for pdf_file in manual_path.glob("*.pdf"):

    print(f"\nLoading {pdf_file.name}")

    namespace = ROUTER_NAMESPACES.get(pdf_file.name)

    if namespace is None:
        print(f"No namespace configured for {pdf_file.name}")
        continue

    print(f"Namespace : {namespace}")

    loader = PyPDFLoader(str(pdf_file))

    documents = loader.load()

    
# -----------------------------
# Split Documents
# -----------------------------

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )


    chunks = text_splitter.split_documents(
    documents
    )


    print(
        f"Total chunks created: {len(chunks)}"
        )


# -----------------------------
# Generate Embeddings
# -----------------------------

    embeddings = OpenAIEmbeddings()


# -----------------------------
# Upload to Pinecone
# -----------------------------

    vectorstore = PineconeVectorStore.from_documents(

        documents=chunks,

        embedding=embeddings,

        index_name=PINECONE_INDEX_NAME,

        namespace=namespace,


    )
    print(f"Uploaded {len(chunks)} chunks to namespace '{namespace}'")


print(
    f"Total pages loaded: {len(documents)}"
)


print(
    "Successfully uploaded documents to Pinecone"
)
