def executive_agent(state):
    """
    Executive Summary Agent
    """

    attack_type = state["detection"]["attack_type"]

    risk_score = state["risk_score"]

    summary = f"""
EXECUTIVE SUMMARY

Incident Type:
{attack_type}

Risk Score:
{risk_score}/100

Business Impact:
Potential unauthorized access
to enterprise accounts.

Recommended Action:
Immediate investigation
and remediation.
"""

    state["executive_summary"] = summary

    return state
