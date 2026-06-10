import os

from langchain_core.documents import Document

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)


# =====================================================
# LOAD KNOWLEDGE BASE FILES
# =====================================================

def load_knowledge_base():

    documents = []

    kb_files = [
        "knowledge_base/mitre_attack.csv",
        "knowledge_base/threat_intelligence.csv"
    ]

    for file_path in kb_files:

        if not os.path.exists(file_path):
            print(f"Missing file: {file_path}")
            continue

        try:

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

        except Exception as e:

            print(
                f"Error reading {file_path}: {e}"
            )

    return documents


# =====================================================
# TEXT SPLITTING
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
# EMBEDDING MODEL
# =====================================================

def create_embeddings():

    embeddings = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings


# =====================================================
# CREATE VECTOR DATABASE
# =====================================================

def build_vector_store():

    print(
        "Building Chroma Vector Store..."
    )

    documents = load_knowledge_base()

    if len(documents) == 0:

        raise ValueError(
            "Knowledge base is empty."
        )

    chunks = split_documents(
        documents
    )

    embeddings = create_embeddings()

    vectordb = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory="./chroma_db"
    )

    print(
        "Vector Store Created Successfully"
    )

    return vectordb


# =====================================================
# LOAD EXISTING VECTOR STORE
# =====================================================

def load_vector_store():

    embeddings = create_embeddings()

    vectordb = Chroma(

        persist_directory="./chroma_db",

        embedding_function=embeddings
    )

    return vectordb


# =====================================================
# GET RETRIEVER
# =====================================================

def get_retriever():

    vectordb = load_vector_store()

    retriever = vectordb.as_retriever(

        search_type="similarity",

        search_kwargs={
            "k": 3
        }
    )

    return retriever


# =====================================================
# INITIALIZE VECTOR STORE
# =====================================================

def initialize_vector_store():

    db_path = "./chroma_db"

    try:

        if not os.path.exists(db_path):

            print(
                "Creating new vector database..."
            )

            build_vector_store()

        else:

            print(
                "Existing vector database found."
            )

        retriever = get_retriever()

        return retriever

    except Exception as e:

        print(
            f"Vector Store Error: {e}"
        )

        raise e
