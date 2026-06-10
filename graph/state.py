from typing import TypedDict


class SOCState(TypedDict):

    dataframe: object

    parsed_logs: dict

    detection: dict

    mitre: dict

    rag_context: str

    threat_intel: str

    remediation: str

    ai_decision: str

    executive_summary: str

    risk_score: int

    report: str
