from utils.llm import get_llm


def remediation_agent(state):
    """
    Remediation Agent

    Generates:
    - Containment Actions
    - Eradication Actions
    - Recovery Actions
    - Long-Term Improvements
    - SOC Recommendations
    """

    llm = get_llm()

    detection = state.get(
        "detection",
        {}
    )

    mitre = state.get(
        "mitre",
        {}
    )

    risk_score = state.get(
        "risk_score",
        0
    )

    threat_intel = state.get(
        "threat_intel",
        ""
    )

    rag_context = state.get(
        "rag_context",
        ""
    )

    prompt = f"""
You are a Senior Incident Response Engineer
working in an Enterprise SOC.

==================================================
DETECTION
==================================================

{detection}

==================================================
MITRE ATT&CK
==================================================

{mitre}

==================================================
RISK SCORE
==================================================

{risk_score}

==================================================
THREAT INTELLIGENCE
==================================================

{threat_intel}

==================================================
RAG CONTEXT
==================================================

{rag_context}

==================================================
TASK
==================================================

Generate a detailed Incident Response Plan.

Include:

1. Immediate Response Actions

2. Containment Actions

3. Eradication Actions

4. Recovery Actions

5. Forensic Investigation Actions

6. Detection Engineering Improvements

7. Security Control Recommendations

8. Long-Term Preventive Measures

9. SOC Team Recommendations

10. Priority Level

Use professional SOC terminology.

Provide actionable recommendations.
"""

    try:

        response = llm.invoke(
            prompt
        )

        remediation_report = (
            response.content
        )

    except Exception as e:

        remediation_report = f"""
INCIDENT RESPONSE PLAN

Remediation Generation Failed

Error:
{str(e)}

Fallback Recommendations

IMMEDIATE ACTIONS

1. Enable MFA

2. Reset affected passwords

3. Block suspicious IP addresses

4. Review authentication logs

5. Investigate affected users

CONTAINMENT

1. Disable compromised accounts

2. Restrict suspicious network activity

3. Monitor related systems

RECOVERY

1. Restore normal access

2. Validate account security

3. Continue monitoring

LONG TERM IMPROVEMENTS

1. Strengthen password policy

2. Enforce MFA

3. Improve threat detection

4. Conduct user awareness training
"""

    state["remediation"] = remediation_report

    return state
