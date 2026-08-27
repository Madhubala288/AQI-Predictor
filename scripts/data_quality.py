"""Data Quality Inspection module for AQI Preprocessing Pipeline."""

from typing import Dict, Any
import pandas as pd


def check_missing_values(df: pd.DataFrame) -> int:
    """Returns total count of missing values across all columns."""
    return int(df.isnull().sum().sum())


def check_duplicates(df: pd.DataFrame) -> int:
    """Returns total count of duplicate rows in the DataFrame."""
    return int(df.duplicated().sum())


def check_empty_dataset(df: pd.DataFrame) -> bool:
    """Checks whether the dataset is empty."""
    return df.empty


def generate_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Generates a detailed Data Quality Summary dictionary."""
    return {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": check_missing_values(df),
        "Duplicate Rows": check_duplicates(df),
        "Is Empty": check_empty_dataset(df)
    }