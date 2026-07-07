import streamlit as st
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from tools.file_reader import FileReader

from tools.data_profiler import DataProfiler

st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyst Agent")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = FileReader.read_csv(uploaded_file)

    st.success("CSV Uploaded Successfully ✅")

#showing the summary of the table
    summary = DataProfiler.get_summary(df)

    st.subheader("📊 Dataset Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", summary["Rows"])

    with col2:
        st.metric("Columns", summary["Columns"])

    with col3:
        st.metric("Missing Values", summary["Missing Values"])

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Duplicate Rows", summary["Duplicate Rows"])

    with col5:
        st.metric("Numeric Columns", summary["Numeric Columns"])

    with col6:
        st.metric("Categorical Columns", summary["Categorical Columns"])

# showing the preview of dataset
    st.subheader("Dataset Preview")

    st.dataframe(df.head())