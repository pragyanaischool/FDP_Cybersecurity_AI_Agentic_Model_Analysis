def mitre_agent(state):
    """
    MITRE ATT&CK Mapping Agent
    """

    attack_type = state["detection"]["attack_type"]

    mitre_mapping = {

        "technique": "N/A",

        "name": "N/A",

        "tactic": "N/A"
    }

    if attack_type == "Password Spraying":

        mitre_mapping = {

            "technique": "T1110.003",

            "name": "Password Spraying",

            "tactic": "Credential Access"
        }

    state["mitre"] = mitre_mapping

    return state
