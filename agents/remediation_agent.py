def remediation_agent(state):
    """
    Remediation Agent

    Generates response recommendations
    based on risk score and attack type.
    """

    attack_type = state["detection"]["attack_type"]

    risk_score = state["risk_score"]

    if risk_score >= 80:

        remediation = f"""
HIGH PRIORITY REMEDIATION

Attack Type:
{attack_type}

Immediate Actions

1. Block malicious source IPs

2. Force password reset for affected users

3. Disable compromised accounts

4. Enable Multi-Factor Authentication

5. Review Active Directory activity

6. Investigate authentication logs

7. Search for lateral movement

8. Notify Incident Response Team

9. Open Priority-1 Incident

10. Preserve logs for forensics
"""

    elif risk_score >= 50:

        remediation = f"""
MEDIUM PRIORITY REMEDIATION

Attack Type:
{attack_type}

Recommended Actions

1. Monitor user accounts

2. Enable MFA

3. Review failed logins

4. Investigate suspicious IPs

5. Increase alerting thresholds

6. Notify SOC Analysts
"""

    else:

        remediation = """
LOW PRIORITY REMEDIATION

1. Continue monitoring

2. Review security logs

3. Maintain existing controls
"""

    state["remediation"] = remediation

    return state
