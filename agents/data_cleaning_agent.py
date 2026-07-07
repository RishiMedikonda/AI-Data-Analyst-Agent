class DataCleaningAgent:

    @staticmethod
    def detect_missing_values(df):

        missing = df.isnull().sum()

        missing = missing[missing > 0]

        return missing