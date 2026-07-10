import pandas as pd
from pandas.api.types import is_string_dtype
import re

 
class DataCleaningAgent:

    #creating a method for detecting the missing values
    @staticmethod
    def detect_missing_values(df):

        missing = df.isnull().sum()

        missing = missing[missing > 0]

        return missing

    #creating a method for detecting the duplicated rows
    @staticmethod
    def detect_duplicate_rows(df):

        return df.duplicated().sum()
    
    #creating a method for retreiving column datatypes
    @staticmethod
    def get_column_datatypes(df):

        return df.dtypes.astype(str)    
    
    #creating a method for detecting the date columns
    @staticmethod
    def detect_date_columns(df):

        date_columns = []
        print(df.dtypes)

        for column in df.columns:
            print(column, df[column].dtype)
        for column in df.columns:

            if is_string_dtype(df[column]):

                converted = pd.to_datetime(df[column], errors="coerce")

                if converted.notna().sum() > 0:
                    date_columns.append(column)

        return date_columns
    
    #creating a method for converting the date columns
    @staticmethod
    def convert_date_columns(df, date_columns):
        for column in date_columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

        return df
    
    #creating a method for filling the missing values
    @staticmethod
    def fill_missing_values(df):

        df = df.copy()

        # Numeric columns
        for column in df.select_dtypes(include="number").columns:

            if df[column].isnull().sum() > 0:
                df[column] = df[column].fillna(df[column].median())

        # Categorical columns
        for column in df.select_dtypes(include=["object", "string"]).columns:

            if df[column].isnull().sum() > 0:
                df[column] = df[column].fillna(df[column].mode()[0])

        return df

    #creating a method for removing duplicate rows
    @staticmethod
    def remove_duplicate_rows(df):

        before = len(df)

        df = df.drop_duplicates()

        after = len(df)

        removed = before - after

        return df, removed
    
    #standardizing the column names using regular expressions

    @staticmethod
    def standardize_column_names(df):

        df = df.copy()

        df.columns = [
            re.sub(r'[^a-zA-Z0-9_]', '', column.strip().lower().replace(" ", "_"))
            for column in df.columns
        ]

        return df
    
    #detecting the outliers

    @staticmethod
    def detect_outliers(df):

        outlier_summary = []

        numeric_columns = df.select_dtypes(include="number").columns

        for column in numeric_columns:

            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            outlier_count = (
                (df[column] < lower_bound) |
                (df[column] > upper_bound)
            ).sum()

            if outlier_count > 0:
                outlier_summary.append({
                    "Column": column,
                    "Outlier Count": int(outlier_count),
                    "Lower Bound": round(lower_bound, 2),
                    "Upper Bound": round(upper_bound, 2)
                })

        return pd.DataFrame(outlier_summary)