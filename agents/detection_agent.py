def detection_agent(state):
    """
    Attack Detection Agent

    Detects:
    - Password Spraying
    - Brute Force
    - Failed Login Attacks
    """

    df = state["dataframe"]

    attack_detected = False
    attack_type = "Normal Activity"

    failed_logins = 0

    if "status" in df.columns:

        failed_logins = len(
            df[
                df["status"]
                .astype(str)
                .str.upper()
                .str.contains(
                    "FAIL",
                    na=False
                )
            ]
        )

    if failed_logins >= 5:

        attack_detected = True

        attack_type = "Password Spraying"

    state["detection"] = {

        "attack_detected": attack_detected,

        "attack_type": attack_type,

        "failed_logins": failed_logins
    }

    return state
