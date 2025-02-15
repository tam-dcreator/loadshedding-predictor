"""
This module provides utility data loading from web resources.
It includes functions to read CSV files from a path.
"""

import pandas as pd
import logging


# Set up basic logging configuration
logger = logging.getLogger('data_ingestion')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - '
                                               '%(levelname)s - %(message)s')


def read_from_CSV(path):
    """
    Reads a CSV file from a path into a pandas DataFrame.

    Parameters:
    - path (str): The path to the CSV file.

    Returns:
    - DataFrame: A pandas DataFrame containing the data from the CSV file.

    Raises:
    - ValueError: If the path does not point to a valid CSV file.
    - Exception: For other issues, including network problems.

    Example:
    >>> new_df = read_from_CSV("./my_data.csv")
    """

    try:
        df = pd.read_csv(path)
        logger.info("CSV file read successfully from the path.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error("The path does not point to a valid CSV file. Please "
                     "check the path and try again.")
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV. Error: {e}")
        raise e
