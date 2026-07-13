import os
import sys

import streamlit as st


# ---------------------------------------------------------
# Project imports
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from agents.data_cleaning_agent import DataCleaningAgent
from agents.dataset_understanding_agent import DatasetUnderstandingAgent
from tools.data_profiler import DataProfiler
from tools.file_reader import FileReader


# ---------------------------------------------------------
# Streamlit configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Load AI agent only once
# ---------------------------------------------------------

@st.cache_resource
def load_dataset_agent():
    return DatasetUnderstandingAgent()


dataset_agent = load_dataset_agent()


# ---------------------------------------------------------
# Reusable UI function
# ---------------------------------------------------------

def display_dataset_summary(summary, title):
    """
    Displays dataset summary using Streamlit metric cards.
    """

    st.subheader(title)

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", summary["Rows"])
    col2.metric("Columns", summary["Columns"])
    col3.metric("Missing Values", summary["Missing Values"])

    col4, col5, col6 = st.columns(3)

    col4.metric("Duplicate Rows", summary["Duplicate Rows"])
    col5.metric("Numeric Columns", summary["Numeric Columns"])
    col6.metric(
        "Categorical Columns",
        summary["Categorical Columns"]
    )


# ---------------------------------------------------------
# Main UI
# ---------------------------------------------------------

st.title("📊 AI Data Analyst Agent")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)


if uploaded_file is not None:

    # -----------------------------------------------------
    # 1. Read original dataset
    # -----------------------------------------------------

    raw_df = FileReader.read_csv(uploaded_file)

    st.success("CSV Uploaded Successfully ✅")


    # -----------------------------------------------------
    # 2. Original dataset summary
    # -----------------------------------------------------

    raw_summary = DataProfiler.get_summary(raw_df)

    display_dataset_summary(
        raw_summary,
        "📊 Original Dataset Summary"
    )


    # -----------------------------------------------------
    # 3. Original dataset preview
    # -----------------------------------------------------

    st.subheader("Original Dataset Preview")

    st.dataframe(
        raw_df.head(),
        use_container_width=True
    )


    # -----------------------------------------------------
    # 4. Detect data-quality issues
    # -----------------------------------------------------

    missing_values = (
        DataCleaningAgent.detect_missing_values(raw_df)
    )

    duplicate_count = (
        DataCleaningAgent.detect_duplicate_rows(raw_df)
    )

    date_columns = (
        DataCleaningAgent.detect_date_columns(raw_df)
    )

    original_datatypes = (
        DataCleaningAgent.get_column_datatypes(raw_df)
    )


    # -----------------------------------------------------
    # 5. Data cleaning report
    # -----------------------------------------------------

    st.subheader("🧹 Data Cleaning Report")

    st.write("### Missing Values")

    if len(missing_values) > 0:
        st.dataframe(
            missing_values,
            use_container_width=True
        )
    else:
        st.success("No Missing Values Found ✅")


    st.write("### Duplicate Rows")

    st.metric(
        "Duplicate Rows",
        duplicate_count
    )


    st.write("### Column Data Types")

    st.dataframe(
        original_datatypes,
        use_container_width=True
    )


    st.write("### Detected Date Columns")

    if date_columns:
        for column in date_columns:
            st.success(f"📅 {column}")
    else:
        st.info("No Date Columns Found")


    # -----------------------------------------------------
    # 6. Create cleaned dataset
    # -----------------------------------------------------

    cleaned_df = raw_df.copy()

    if date_columns:
        cleaned_df = (
            DataCleaningAgent.convert_date_columns(
                cleaned_df,
                date_columns
            )
        )

    cleaned_df = (
        DataCleaningAgent.fill_missing_values(cleaned_df)
    )

    cleaned_df, removed_duplicates = (
        DataCleaningAgent.remove_duplicate_rows(cleaned_df)
    )

    cleaned_df = (
        DataCleaningAgent.standardize_column_names(
            cleaned_df
        )
    )


    # -----------------------------------------------------
    # 7. Cleaning results
    # -----------------------------------------------------

    st.write("### Duplicate Cleaning")

    if removed_duplicates > 0:
        st.success(
            f"Removed {removed_duplicates} duplicate rows ✅"
        )
    else:
        st.success("No duplicate rows to remove ✅")


    st.subheader("Cleaned Dataset Preview")

    st.dataframe(
        cleaned_df.head(),
        use_container_width=True
    )


    cleaned_summary = DataProfiler.get_summary(cleaned_df)

    display_dataset_summary(
        cleaned_summary,
        "📊 Cleaned Dataset Summary"
    )


    # -----------------------------------------------------
    # 8. Outlier detection
    # -----------------------------------------------------

    outliers = DataCleaningAgent.detect_outliers(
        cleaned_df
    )

    st.subheader("Outlier Detection")

    if not outliers.empty:

        st.warning(
            f"Outliers were detected in "
            f"{len(outliers)} numeric column(s)."
        )

        st.dataframe(
            outliers,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success("No outliers detected ✅")


    # -----------------------------------------------------
    # 9. AI dataset understanding
    # -----------------------------------------------------

    st.subheader("🤖 AI Dataset Understanding")

    if st.button(
        "Analyze Dataset with AI",
        type="primary"
    ):

        with st.spinner(
            "AI is analyzing the cleaned dataset..."
        ):

            try:

                analysis = dataset_agent.analyze(
                    cleaned_df
                )

                st.markdown(analysis)

            except Exception as error:

                st.error(
                    f"AI analysis failed: {error}"
                )