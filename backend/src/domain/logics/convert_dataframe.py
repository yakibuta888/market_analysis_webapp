# src/domain/logics/convert_dataframe.py
import pandas as pd
from typing import Any


def dataframe_to_json(df: pd.DataFrame) -> dict[str, Any]:
    """
    Converts a DataFrame to a JSON object.

    Args:
        df (pd.DataFrame): A DataFrame to convert to a JSON object.

    Returns:
        dict[str, Any]: A JSON object converted from the DataFrame.
    """
    data_list = df.to_dict('records')

    response_data = {
        "data": data_list
    }

    return response_data


def to_year_month_format(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Converts a column in a DataFrame to a year-month format.

    Args:
        df (pd.DataFrame): A DataFrame to convert the column.
        column_name (str): The name of the column to convert.

    Returns:
        pd.DataFrame: A DataFrame with the column converted to a year-month format.
    """
    df[column_name] = df[column_name].dt.strftime('%Y-%m')
    return df
