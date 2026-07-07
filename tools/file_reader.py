import pandas as pd


class FileReader:
    """
    Utility class for reading different file formats.
    """

    @staticmethod
    def read_csv(file):
        """
        Reads a CSV file and returns a pandas DataFrame.
        """
        return pd.read_csv(file)