from rag.retrieval import get_rag_context


def rag_agent(state):
    """
    RAG Knowledge Agent

    Retrieves cyber security context from
    the vector database and enriches the
    investigation workflow.
    """

    # =====================================
    # CHECK RETRIEVER
    # =====================================

    retriever = state.get("retriever")

    if retriever is None:

        state["rag_context"] = """
Cyber Security Knowledge Base

Password Spraying:
Attempts common passwords against
multiple user accounts.

Indicators:
- Multiple failed logins
- Same source IP
- Many target accounts

Recommended Actions:
- Enable MFA
- Reset Passwords
- Block Source IP
- Investigate Accounts
"""

        return state

    # =====================================
    # GET ATTACK TYPE
    # =====================================

    detection = state.get(
        "detection",
        {}
    )

    attack_type = detection.get(
        "attack_type",
        "Unknown Threat"
    )

    # =====================================
    # RAG RETRIEVAL
    # =====================================

    try:

        context = get_rag_context(
            retriever,
            attack_type
        )

        if context is None:

            context = ""

        if len(str(context).strip()) == 0:

            context = f"""
Threat Type:
{attack_type}

No matching knowledge found in
vector database.

Recommended:
Review threat intelligence feeds
and MITRE ATT&CK mapping.
"""

        state["rag_context"] = context

    except Exception as e:

        state["rag_context"] = f"""
RAG Retrieval Error

Attack Type:
{attack_type}

Error:
{str(e)}

Fallback Knowledge

Password Spraying:
Attempts common passwords
against multiple users.

Recommended:
Enable MFA
Reset Passwords
Investigate Source IP
"""

    return state
