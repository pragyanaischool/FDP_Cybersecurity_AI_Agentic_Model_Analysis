import streamlit as st
import pandas as pd
import plotly.express as px

from graph.workflow import app

from rag.vector_store import (
    initialize_vector_store
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Autonomous AI SOC",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title(
    "🛡️ Autonomous Multi-Agent AI SOC"
)

st.markdown(
    """
    GenAI + RAG + LangGraph Powered
    Security Operations Center
    """
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header(
    "SOC Controls"
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Security Logs",
    type=["csv"]
)

# =====================================================
# LOAD VECTOR DB
# =====================================================

@st.cache_resource
def load_retriever():

    return initialize_vector_store()

retriever = load_retriever()

# =====================================================
# PROCESS LOG FILE
# =====================================================

if uploaded_file is not None:

    df = pd.read_csv(
        uploaded_file
    )

    st.success(
        "Log file uploaded successfully"
    )

    # =================================================
    # DASHBOARD
    # =================================================

    st.header(
        "Security Dashboard"
    )

    total_logs = len(df)

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

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Events",
        total_logs
    )

    col2.metric(
        "Failed Logins",
        failed_logins
    )

    # =================================================
    # RAW DATA
    # =================================================

    with st.expander(
        "View Raw Logs"
    ):

        st.dataframe(
            df,
            use_container_width=True
        )

    # =================================================
    # VISUALIZATION
    # =================================================

    st.header(
        "Threat Analytics"
    )

    if "status" in df.columns:

        status_counts = (
            df["status"]
            .astype(str)
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Status",
            "Count"
        ]

        fig = px.bar(
            status_counts,
            x="Status",
            y="Count",
            title="Authentication Events"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =================================================
    # RUN AI INVESTIGATION
    # =================================================

    if st.button(
        "🚀 Run Autonomous Investigation"
    ):

        with st.spinner(
            "Running AI Agents..."
        ):

            result = app.invoke(
                {
                    "dataframe": df,
                    "retriever": retriever
                }
            )

        st.success(
            "Investigation Completed"
        )

        # =============================================
        # AGENT OUTPUTS
        # =============================================

        st.header(
            "AI Investigation Results"
        )

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Report",
                "MITRE",
                "Threat Intel",
                "Executive Summary"
            ]
        )

        with tab1:

            st.text_area(
                "SOC Report",
                result["report"],
                height=500
            )

        with tab2:

            st.json(
                result["mitre"]
            )

        with tab3:

            st.text_area(
                "Threat Intelligence",
                result["threat_intel"],
                height=250
            )

        with tab4:

            st.text_area(
                "Executive Summary",
                result["executive_summary"],
                height=250
            )

        # =============================================
        # RISK SCORE
        # =============================================

        st.header(
            "Risk Assessment"
        )

        risk_score = result[
            "risk_score"
        ]

        st.progress(
            risk_score / 100
        )

        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )

        # =============================================
        # DOWNLOAD REPORT
        # =============================================

        st.download_button(
            label="Download SOC Report",
            data=result["report"],
            file_name="soc_report.txt",
            mime="text/plain"
        )

else:

    st.info(
        "Upload a CSV log file to begin investigation."
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Autonomous Multi-Agent AI SOC | GenAI + LangGraph + RAG"
)
