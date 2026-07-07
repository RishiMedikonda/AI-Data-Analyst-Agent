import pandas as pd


class DataProfiler:

    @staticmethod
    def get_summary(df):

        summary = {

            "Rows": df.shape[0],

            "Columns": df.shape[1],

            "Missing Values": df.isnull().sum().sum(),

            "Duplicate Rows": df.duplicated().sum(),

            "Numeric Columns": len(df.select_dtypes(include="number").columns),

            "Categorical Columns": len(df.select_dtypes(include="object").columns)

        }

        return summary