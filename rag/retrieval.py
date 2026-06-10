from typing import List


# =====================================================
# Retrieve Documents
# =====================================================

def retrieve_documents(
    retriever,
    query: str
) -> List:

    try:

        documents = retriever.invoke(
            query
        )

        return documents

    except Exception as e:

        print(
            f"Retrieval Error: {e}"
        )

        return []


# =====================================================
# Convert Documents To Context
# =====================================================

def documents_to_context(
    documents: List
) -> str:

    if not documents:

        return "No relevant context found."

    context_parts = []

    for doc in documents:

        context_parts.append(
            doc.page_content
        )

    return "\n\n".join(
        context_parts
    )


# =====================================================
# Retrieve Context
# =====================================================

def retrieve_context(
    retriever,
    query: str
) -> str:

    documents = retrieve_documents(
        retriever,
        query
    )

    context = documents_to_context(
        documents
    )

    return context


# =====================================================
# Retrieve With Metadata
# =====================================================

def retrieve_context_with_sources(
    retriever,
    query: str
):

    documents = retrieve_documents(
        retriever,
        query
    )

    results = []

    for doc in documents:

        results.append(
            {
                "content":
                doc.page_content,

                "source":
                doc.metadata.get(
                    "source",
                    "Unknown"
                )
            }
        )

    return results


# =====================================================
# Cyber Security Search
# =====================================================

def search_threat_intelligence(
    retriever,
    attack_type: str
):

    query = f"""
    Cyber Security Threat Intelligence
    Attack Type:
    {attack_type}
    """

    return retrieve_context(
        retriever,
        query
    )


# =====================================================
# MITRE Search
# =====================================================

def search_mitre_attack(
    retriever,
    technique_name: str
):

    query = f"""
    MITRE ATTACK Technique
    {technique_name}
    """

    return retrieve_context(
        retriever,
        query
    )


# =====================================================
# Incident Investigation Search
# =====================================================

def search_incident_context(
    retriever,
    attack_type: str
):

    query = f"""
    Security Incident Investigation

    Attack:
    {attack_type}

    Detection Indicators

    Risk

    Remediation
    """

    return retrieve_context(
        retriever,
        query
    )


# =====================================================
# Main RAG Function
# =====================================================

def get_rag_context(
    retriever,
    attack_type: str
):

    context = search_incident_context(
        retriever,
        attack_type
    )

    return context
