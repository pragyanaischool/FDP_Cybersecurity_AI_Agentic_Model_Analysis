def autonomous_response_agent(state):
    """
    Autonomous Response Agent
    """

    risk_score = state["risk_score"]

    if risk_score >= 80:

        action = """
HIGH RISK

BLOCK SOURCE IP

DISABLE ACCOUNT

OPEN P1 INCIDENT

NOTIFY SOC TEAM
"""

    elif risk_score >= 50:

        action = """
MEDIUM RISK

ESCALATE TO ANALYST

CONTINUE MONITORING
"""

    else:

        action = """
LOW RISK

MONITOR ONLY
"""

    state["ai_decision"] = action

    return state
