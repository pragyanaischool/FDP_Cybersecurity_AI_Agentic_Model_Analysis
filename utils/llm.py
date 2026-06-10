import streamlit as st

from langchain_groq import ChatGroq


def get_llm():

    try:

        groq_api_key = st.secrets[
            "GROQ_API_KEY"
        ]

    except Exception:

        raise ValueError(
            """
GROQ_API_KEY not found.

Add it to:

.streamlit/secrets.toml

Example:

GROQ_API_KEY="gsk_xxxxx"
"""
        )

    llm = ChatGroq(

        groq_api_key=groq_api_key,

        model="llama-3.3-70b-versatile",

        temperature=0,

        max_tokens=2048
    )

    return llm
