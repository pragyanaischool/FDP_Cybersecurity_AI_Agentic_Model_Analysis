from langgraph.graph import StateGraph, END

from graph.state import SOCState

from agents.parser_agent import parser_agent
from agents.detection_agent import detection_agent
from agents.mitre_agent import mitre_agent
from agents.rag_agent import rag_agent
from agents.threat_intel_agent import threat_intelligence_agent
from agents.remediation_agent import remediation_agent
from agents.autonomous_response_agent import autonomous_response_agent
from agents.executive_agent import executive_agent


# =====================================================
# Risk Scoring Agent
# =====================================================

def risk_scoring_agent(state):

    detection = state["detection"]

    if detection["attack_detected"]:

        score = 90

    else:

        score = 10

    state["risk_score"] = score

    return state


# =====================================================
# Final Report Agent
# =====================================================

def report_agent(state):

    report = f"""
==================================================
AUTONOMOUS MULTI-AGENT AI SOC REPORT
==================================================

ATTACK DETECTION
--------------------------------------------------
Attack Detected:
{state["detection"]["attack_detected"]}

Attack Type:
{state["detection"]["attack_type"]}


MITRE ATT&CK MAPPING
--------------------------------------------------
Technique:
{state["mitre"]["technique"]}

Technique Name:
{state["mitre"]["name"]}

Tactic:
{state["mitre"]["tactic"]}


RISK SCORE
--------------------------------------------------
{state["risk_score"]}/100


THREAT INTELLIGENCE
--------------------------------------------------
{state["threat_intel"]}


REMEDIATION PLAN
--------------------------------------------------
{state["remediation"]}


AUTONOMOUS RESPONSE
--------------------------------------------------
{state["ai_decision"]}


EXECUTIVE SUMMARY
--------------------------------------------------
{state["executive_summary"]}


RAG KNOWLEDGE CONTEXT
--------------------------------------------------
{state["rag_context"]}

==================================================
END OF REPORT
==================================================
"""

    state["report"] = report

    return state


# =====================================================
# Build Graph
# =====================================================

workflow = StateGraph(SOCState)

workflow.add_node(
    "parser",
    parser_agent
)

workflow.add_node(
    "detect",
    detection_agent
)

workflow.add_node(
    "mitre",
    mitre_agent
)

workflow.add_node(
    "rag",
    rag_agent
)

workflow.add_node(
    "risk",
    risk_scoring_agent
)

workflow.add_node(
    "intel",
    threat_intelligence_agent
)

workflow.add_node(
    "remediation",
    remediation_agent
)

workflow.add_node(
    "response",
    autonomous_response_agent
)

workflow.add_node(
    "executive",
    executive_agent
)

workflow.add_node(
    "report",
    report_agent
)


# =====================================================
# Workflow
# =====================================================

workflow.set_entry_point(
    "parser"
)

workflow.add_edge(
    "parser",
    "detect"
)

workflow.add_edge(
    "detect",
    "mitre"
)

workflow.add_edge(
    "mitre",
    "rag"
)

workflow.add_edge(
    "rag",
    "risk"
)

workflow.add_edge(
    "risk",
    "intel"
)

workflow.add_edge(
    "intel",
    "remediation"
)

workflow.add_edge(
    "remediation",
    "response"
)

workflow.add_edge(
    "response",
    "executive"
)

workflow.add_edge(
    "executive",
    "report"
)

workflow.add_edge(
    "report",
    END
)


# =====================================================
# Compile Graph
# =====================================================

app = workflow.compile()
