def threat_intelligence_agent(state):
    """
    Threat Intelligence Agent
    """

    attack_type = state["detection"]["attack_type"]

    threat_intel = f"""
Threat Intelligence Analysis

Detected Threat:
{attack_type}

Threat Category:
Credential Access

Potential Objectives:
- Credential Theft
- Initial Access
- Account Compromise

Recommended Monitoring:
- Failed Logins
- Source IP Addresses
- MFA Events
"""

    state["threat_intel"] = threat_intel

    return state
