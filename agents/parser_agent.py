import pandas as pd


def parser_agent(state):
    """
    Log Parsing Agent

    Responsibilities:
    - Validate uploaded log data
    - Extract metadata
    - Generate basic statistics
    """

    df = state["dataframe"]

    parsed_logs = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "sample_records": df.head(5).to_dict(
            orient="records"
        )
    }

    state["parsed_logs"] = parsed_logs

    return state
