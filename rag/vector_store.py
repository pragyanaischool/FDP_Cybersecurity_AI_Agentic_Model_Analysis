import os

from langchain.docstore.document import Document

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)


# =====================================================
# Load Knowledge Base Files
# =====================================================

def load_knowledge_base():

    documents = []

    kb_files = [
        "knowledge_base/mitre_attack.csv",
        "knowledge_base/threat_intelligence.csv"
    ]

    for file_path in kb_files:

        if not os.path.exists(file_path):
            continue

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path
                }
            )
        )

    return documents


# =====================================================
# Split Documents
# =====================================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks


# =====================================================
# Create Embeddings
# =====================================================

def create_embeddings():

    embeddings = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings


# =====================================================
# Build Chroma Vector Store
# =====================================================

def build_vector_store():

    documents = load_knowledge_base()

    chunks = split_documents(
        documents
    )

    embeddings = create_embeddings()

    vectordb = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory="./chroma_db"
    )

    return vectordb


# =====================================================
# Get Retriever
# =====================================================

def get_retriever():

    embeddings = create_embeddings()

    vectordb = Chroma(

        persist_directory="./chroma_db",

        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(

        search_type="similarity",

        search_kwargs={
            "k": 3
        }
    )

    return retriever


# =====================================================
# Initialize KB
# =====================================================

def initialize_vector_store():

    if not os.path.exists("./chroma_db"):

        print(
            "Creating Vector Database..."
        )

        build_vector_store()

        print(
            "Vector Database Created."
        )

    else:

        print(
            "Using Existing Vector Database."
        )

    retriever = get_retriever()

    return retriever
