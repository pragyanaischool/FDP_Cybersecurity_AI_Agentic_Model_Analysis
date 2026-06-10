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
# SESSION STATE
# =====================================================

if "df" not in st.session_state:
    st.session_state.df = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

if "investigation_result" not in st.session_state:
    st.session_state.investigation_result = None


# =====================================================
# LOAD RETRIEVER
# =====================================================

@st.cache_resource
def load_retriever():

    return initialize_vector_store()


retriever = load_retriever()


# =====================================================
# HEADER
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
# FILE MEMORY
# =====================================================

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        st.session_state.df = df

        st.session_state.uploaded_filename = (
            uploaded_file.name
        )

        st.sidebar.success(
            f"Loaded: {uploaded_file.name}"
        )

    except Exception as e:

        st.error(
            f"File Error: {str(e)}"
        )

# =====================================================
# USE SAVED FILE
# =====================================================

if st.session_state.df is not None:

    df = st.session_state.df

    st.info(
        f"Using File: "
        f"{st.session_state.uploaded_filename}"
    )

    # =================================================
    # KPI DASHBOARD
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
    # INVESTIGATION BUTTON
    # =================================================

    if st.button(
        "🚀 Run Autonomous Investigation"
    ):

        with st.spinner(
            "Running AI Agents..."
        ):

            try:

                result = app.invoke(
                    {
                        "dataframe": df,
                        "retriever": retriever
                    }
                )

                st.session_state.investigation_result = (
                    result
                )

                st.success(
                    "Investigation Completed"
                )

            except Exception as e:

                st.error(
                    f"Investigation Error:\n{str(e)}"
                )

    # =================================================
    # SHOW PREVIOUS RESULT
    # =================================================

    if (
        st.session_state.investigation_result
        is not None
    ):

        result = (
            st.session_state.investigation_result
        )

        st.header(
            "AI Investigation Results"
        )

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "SOC Report",
                "MITRE",
                "Threat Intel",
                "Executive"
            ]
        )

        # =============================================
        # REPORT
        # =============================================

        with tab1:

            st.text_area(
                "SOC Report",
                result.get(
                    "report",
                    ""
                ),
                height=500
            )

        # =============================================
        # MITRE
        # =============================================

        with tab2:

            st.json(
                result.get(
                    "mitre",
                    {}
                )
            )

        # =============================================
        # THREAT INTEL
        # =============================================

        with tab3:

            st.text_area(
                "Threat Intelligence",
                result.get(
                    "threat_intel",
                    ""
                ),
                height=250
            )

        # =============================================
        # EXECUTIVE
        # =============================================

        with tab4:

            st.text_area(
                "Executive Summary",
                result.get(
                    "executive_summary",
                    ""
                ),
                height=250
            )

        # =============================================
        # RISK SCORE
        # =============================================

        risk_score = result.get(
            "risk_score",
            0
        )

        st.header(
            "Risk Assessment"
        )

        st.progress(
            min(
                risk_score / 100,
                1.0
            )
        )

        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )

        # =============================================
        # DOWNLOAD
        # =============================================

        st.download_button(
            label="Download Report",
            data=result.get(
                "report",
                ""
            ),
            file_name="soc_report.txt",
            mime="text/plain"
        )

# =====================================================
# EMPTY STATE
# =====================================================

else:

    st.info(
        "Upload a CSV file to begin."
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Autonomous Multi-Agent AI SOC | "
    "LangGraph + RAG + Streamlit"
)
