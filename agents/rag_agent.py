from rag.retrieval import get_rag_context


def rag_agent(state):
    """
    RAG Knowledge Agent
    """

    retriever = state["retriever"]

    attack_type = state["detection"]["attack_type"]

    context = get_rag_context(
        retriever=retriever,
        attack_type=attack_type
    )

    state["rag_context"] = context

    return state
