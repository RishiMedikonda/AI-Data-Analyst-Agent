import streamlit as st
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from tools.file_reader import FileReader
from tools.data_profiler import DataProfiler
from agents.data_cleaning_agent import DataCleaningAgent
from agents.dataset_understanding_agent import DatasetUnderstandingAgent

@st.cache_resource
def load_dataset_agent():
    return DatasetUnderstandingAgent()

dataset_agent = load_dataset_agent()


st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Agent")
#st.title("📊 AI Data Analyst Agent")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = FileReader.read_csv(uploaded_file)
    #st.write(df.dtypes)
    # st.write(df["Date"].dtype)
    # st.write(df["Date"].head())
    # st.write(df["Date"].iloc[0])
    # st.write(type(df["Date"].iloc[0]))


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


    missing = DataCleaningAgent.detect_missing_values(df)

    duplicates = DataCleaningAgent.detect_duplicate_rows(df)

    date_columns = DataCleaningAgent.detect_date_columns(df)

    df = DataCleaningAgent.convert_date_columns(df, date_columns)

    datatypes = DataCleaningAgent.get_column_datatypes(df)
    df = DataCleaningAgent.fill_missing_values(df)

    df, removed_duplicates = DataCleaningAgent.remove_duplicate_rows(df)

    df = DataCleaningAgent.standardize_column_names(df)

    outliers = DataCleaningAgent.detect_outliers(df)
    
# showing the preview of dataset
    st.subheader("Dataset Preview")

    st.dataframe(df.head())

# data cleaning
    st.subheader("🧹 Data Cleaning Report")
    st.write("### Missing Values")

    if len(missing) > 0:
        st.dataframe(missing)
    else:
        st.success("No Missing Values Found ✅")

    st.write("### Duplicate Rows")
    st.metric("Duplicate Rows", duplicates)

    st.write("### Column Data Types")
    st.dataframe(datatypes)

    st.write("### Detected Date Columns")

    if date_columns:
        for col in date_columns:
            st.success(f"📅 {col}")
    else:
        st.info("No Date Columns Found")

    st.write("### Duplicate Cleaning")

    if removed_duplicates > 0:
        st.success(f"Removed {removed_duplicates} duplicate rows ✅")
    else:
        st.success("No duplicate rows to remove ✅")

    st.write("### Cleaned Dataset")

    st.dataframe(df.head())

#getting summary of Cleaned Data Set

    summary = DataProfiler.get_summary(df)
    st.subheader("📊 Cleaned Dataset Summary")

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

    
    #displaying outliers

    st.write("### Outlier Detection")

    if not outliers.empty:
        st.warning(
            f"Outliers were detected in {len(outliers)} numeric column(s)."
        )

        st.dataframe(
            outliers,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("No outliers detected ✅")


    st.subheader("🤖 AI Dataset Understanding")

    if st.button("Analyze Dataset with AI"):

        with st.spinner("AI is analyzing the dataset..."):

            analysis = dataset_agent.analyze(df)

            st.markdown(analysis)