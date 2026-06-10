from utils.llm import get_llm


def threat_intelligence_agent(state):
    """
    Threat Intelligence Agent

    Uses:
    - Detection Results
    - MITRE ATT&CK Mapping
    - RAG Knowledge Base

    Generates:
    - Threat Assessment
    - Severity Analysis
    - Indicators of Compromise
    - Adversary Objectives
    - Recommendations
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

    rag_context = state.get(
        "rag_context",
        ""
    )

    attack_type = detection.get(
        "attack_type",
        "Unknown Threat"
    )

    prompt = f"""
You are a Senior Cyber Threat Intelligence Analyst
working inside an Enterprise SOC.

Analyze the security incident.

==================================================
DETECTION
==================================================

{detection}

==================================================
MITRE ATT&CK
==================================================

{mitre}

==================================================
RAG KNOWLEDGE BASE
==================================================

{rag_context}

==================================================
TASK
==================================================

Generate a professional Threat Intelligence Report.

Include:

1. Executive Threat Assessment

2. Threat Classification

3. MITRE ATT&CK Analysis

4. Indicators of Compromise (IOCs)

5. Possible Adversary Objectives

6. Impact Assessment

7. Risk Level
   (Low / Medium / High / Critical)

8. Recommended Investigation Steps

9. Recommended Monitoring Actions

10. Recommended Containment Actions

Keep the report concise,
professional and SOC-ready.
"""

    try:

        response = llm.invoke(
            prompt
        )

        threat_report = response.content

    except Exception as e:

        threat_report = f"""
THREAT INTELLIGENCE REPORT

Attack Type:
{attack_type}

Threat Intelligence Generation Failed

Error:
{str(e)}

Fallback Assessment

Risk Level:
High

Recommended Actions:

1. Review authentication logs

2. Investigate source IPs

3. Enable MFA

4. Reset affected credentials

5. Monitor suspicious activity
"""

    state["threat_intel"] = threat_report

    return state
