"""Automated Unit Tests for Data Quality Utilities."""

import sys
from pathlib import Path
import pandas as pd

# Path fix so pytest can locate modules in scripts directory
sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))

from data_quality import (
    check_missing_values,
    check_duplicates,
    check_empty_dataset,
    generate_summary,
)


def test_missing_values():
    """Verify that missing value counter accurate works."""
    data = {"Temperature": [25.0, None, 30.0], "AQI": [100, 120, None]}
    df = pd.DataFrame(data)
    assert check_missing_values(df) == 2


def test_duplicates():
    """Verify duplicate row detection."""
    data = {"City": ["Karachi", "Karachi"], "AQI": [150, 150]}
    df = pd.DataFrame(data)
    assert check_duplicates(df) == 1


def test_empty_dataset():
    """Verify empty dataframe checking."""
    df_empty = pd.DataFrame()
    df_filled = pd.DataFrame({"AQI": [100]})

    assert check_empty_dataset(df_empty) is True
    assert check_empty_dataset(df_filled) is False


def test_generate_summary():
    """Verify quality summary dictionary structure and calculations."""
    data = {"AQI": [100, 120, 100], "City": ["Lahore", "Lahore", "Lahore"]}
    df = pd.DataFrame(data)
    summary = generate_summary(df)

    assert summary["Rows"] == 3
    assert summary["Columns"] == 2
    assert summary["Missing Values"] == 0
    assert summary["Duplicate Rows"] == 1
    assert summary["Is Empty"] is False