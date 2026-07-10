from typing import Any

import pandas as pd
from langchain_ollama import ChatOllama


class DatasetUnderstandingAgent:
    """
    Uses a local Ollama LLM to explain the uploaded dataset.
    """

    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.1:latest",
            temperature=0
        )

    @staticmethod
    def prepare_dataset_context(df: pd.DataFrame) -> dict[str, Any]:
        """
        Creates compact dataset information for the LLM.
        The complete dataset is not sent to the model.
        """

        numeric_columns = df.select_dtypes(include="number").columns.tolist()

        categorical_columns = df.select_dtypes(
            include=["object", "string", "category"]
        ).columns.tolist()

        datetime_columns = df.select_dtypes(
            include=["datetime", "datetimetz"]
        ).columns.tolist()

        unique_values = {
            column: int(df[column].nunique(dropna=True))
            for column in df.columns
        }

        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "datetime_columns": datetime_columns,
            "missing_values": {
                column: int(value)
                for column, value in df.isnull().sum().items()
                if value > 0
            },
            "duplicate_rows": int(df.duplicated().sum()),
            "unique_values": unique_values,
            "sample_rows": df.head(5).astype(str).to_dict(orient="records")
        }

    def analyze(self, df: pd.DataFrame) -> str:
        """
        Sends dataset metadata to the local LLM and returns an explanation.
        """

        context = self.prepare_dataset_context(df)

        prompt = f"""
You are a senior data analyst.

Analyze the following dataset metadata.

Dataset metadata:
{context}

Provide the response using these headings:

1. Dataset Overview
2. Important Columns
3. Possible Target Column
4. Data Quality Observations
5. Recommended Analyses
6. Possible Machine Learning Problem

Rules:
- Use only the supplied metadata.
- Do not invent business meaning.
- Clearly mention when the dataset purpose is uncertain.
- Keep the explanation simple and practical.
- Do not claim that a column is definitely the target.
- Suggest a target column only when there is reasonable evidence.
"""

        response = self.llm.invoke(prompt)

        return str(response.content)