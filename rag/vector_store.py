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
# LOAD KNOWLEDGE BASE
# =====================================================

def load_knowledge_base():

    documents = []

    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    project_root = os.path.dirname(
        current_dir
    )

    kb_files = [

        os.path.join(
            project_root,
            "knowledge_base",
            "mitre_attack.csv"
        ),

        os.path.join(
            project_root,
            "knowledge_base",
            "threat_intelligence.csv"
        )
    ]

    for file_path in kb_files:

        if not os.path.exists(file_path):

            print(
                f"Missing KB File: {file_path}"
            )

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

    # -----------------------------------------
    # Fallback if KB is empty
    # -----------------------------------------

    if len(documents) == 0:

        documents = [

            Document(

                page_content="""
Password Spraying

Attempts common passwords
against many user accounts.

Indicators

- Multiple failed logins
- Same source IP
- Many target accounts

Recommended Actions

- Enable MFA
- Reset Passwords
- Block Source IP
""",

                metadata={
                    "source": "default"
                }
            )
        ]

    return documents


# =====================================================
# SPLIT DOCUMENTS
# =====================================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50
    )

    return splitter.split_documents(
        documents
    )


# =====================================================
# EMBEDDINGS
# =====================================================

def create_embeddings():

    return HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )


# =====================================================
# BUILD VECTOR STORE
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
# LOAD VECTOR STORE
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
                "Creating ChromaDB..."
            )

            build_vector_store()

        retriever = get_retriever()

        return retriever

    except Exception as e:

        print(
            f"Vector Store Error: {e}"
        )

        return None
