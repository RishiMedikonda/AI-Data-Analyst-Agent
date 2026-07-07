class DataCleaningAgent:

    @staticmethod
    def detect_missing_values(df):

        missing = df.isnull().sum()

        missing = missing[missing > 0]

        return missing

    @staticmethod
    def detect_duplicate_rows(df):

        return df.duplicated().sum()
    
    @staticmethod
    def get_column_datatypes(df):

        return df.dtypes
    
    @staticmethod
    def detect_date_columns(df):

        date_columns = []

        for column in df.columns:

            try:
                pd.to_datetime(df[column])

                date_columns.append(column)

            except:

                pass

        return date_columns