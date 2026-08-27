"""Production-Ready Data Preprocessing Pipeline with Data Quality Assurance."""

import logging
from typing import Optional

import pandas as pd

from config import HISTORICAL_DATA, PROCESSED_DATA, REQUIRED_COLUMNS
from data_quality import generate_summary


# ============================================================
# Logging Configuration
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


# ============================================================
# Step 1 — Load Dataset
# ============================================================

def load_data(path) -> Optional[pd.DataFrame]:
    """Loads historical dataset from CSV."""

    try:
        logging.info(f"Loading dataset from: {path}")

        df = pd.read_csv(path)

        logging.info("Dataset loaded successfully.")

        return df

    except FileNotFoundError:
        logging.error(f"File not found at path: {path}")
        return None

    except Exception as error:
        logging.error(
            f"Unexpected error loading dataset: {str(error)}"
        )
        return None


# ============================================================
# Step 2 — Validate Dataset
# ============================================================

def validate_dataset(df: pd.DataFrame) -> None:
    """Validates dataset structure and required columns."""

    if df is None or df.empty:
        raise ValueError(
            "Dataset validation failed: DataFrame is empty or null."
        )

    missing_cols = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_cols:
        raise ValueError(
            f"Dataset validation failed. "
            f"Missing required columns: {missing_cols}"
        )

    logging.info("Dataset schema validation successful.")


# ============================================================
# Step 3 — Handle Missing Values
# ============================================================

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles missing values.

    Numeric columns:
    Median imputation.

    Categorical columns:
    'Unknown' value.
    """

    # Numeric columns
    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns

    for col in numeric_columns:

        if df[col].isnull().sum() > 0:

            df[col] = df[col].fillna(
                df[col].median()
            )

    # Categorical columns
    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for col in categorical_columns:

        if df[col].isnull().sum() > 0:

            df[col] = df[col].fillna("Unknown")

    logging.info("Missing values handled.")

    return df


# ============================================================
# Step 4 — Remove Duplicates
# ============================================================

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate rows."""

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    logging.info(
        f"Removed {removed} duplicate rows."
    )

    return df


# ============================================================
# Step 5 — Fix Data Types
# ============================================================

def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts Timestamp column to datetime.

    The actual Karachi dataset uses 'Timestamp'
    instead of 'Date'.
    """

    if "Timestamp" in df.columns:

        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce",
            utc=True
        )

        # Remove rows where timestamp could not be converted
        invalid_timestamps = df["Timestamp"].isnull().sum()

        if invalid_timestamps > 0:

            logging.warning(
                f"Removing {invalid_timestamps} rows "
                f"with invalid timestamps."
            )

            df = df.dropna(
                subset=["Timestamp"]
            )

        logging.info(
            "Timestamp column converted to datetime successfully."
        )

    return df


# ============================================================
# Step 6 — Sort Dataset
# ============================================================

def sort_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Sorts dataset chronologically."""

    if "Timestamp" in df.columns:

        df = df.sort_values(
            by="Timestamp"
        )

        df = df.reset_index(
            drop=True
        )

        logging.info(
            "Dataset sorted chronologically."
        )

    return df


# ============================================================
# Step 7 — Data Quality Report
# ============================================================

def print_quality_report(summary: dict) -> None:
    """Prints final data quality summary."""

    print(
        "\n"
        + "=" * 10
        + " DATA QUALITY REPORT "
        + "=" * 10
    )

    for key, value in summary.items():

        print(
            f"{key:<20}: {value}"
        )

    print("=" * 41)
    print()


# ============================================================
# Step 8 — Save Processed Dataset
# ============================================================

def save_data(df: pd.DataFrame, path) -> None:
    """Saves processed dataset safely."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        path,
        index=False
    )

    logging.info(
        f"Clean dataset saved to: {path}"
    )


# ============================================================
# Main Pipeline
# ============================================================

def main() -> None:
    """Runs complete preprocessing pipeline."""

    print("\n")
    print("=" * 60)
    print("AQI DATA PREPROCESSING PIPELINE")
    print("=" * 60)

    # Load data
    df = load_data(HISTORICAL_DATA)

    if df is None:
        logging.error(
            "Pipeline terminated."
        )
        return

    try:

        # ------------------------------------
        # 1. Validate dataset
        # ------------------------------------

        validate_dataset(df)

        # ------------------------------------
        # 2. Handle missing values
        # ------------------------------------

        df = handle_missing_values(df)

        # ------------------------------------
        # 3. Remove duplicates
        # ------------------------------------

        df = remove_duplicates(df)

        # ------------------------------------
        # 4. Fix data types
        # ------------------------------------

        df = fix_data_types(df)

        # ------------------------------------
        # 5. Sort chronologically
        # ------------------------------------

        df = sort_dataset(df)

        # ------------------------------------
        # 6. Generate quality report
        # ------------------------------------

        summary = generate_summary(df)

        print_quality_report(summary)

        # ------------------------------------
        # 7. Save cleaned dataset
        # ------------------------------------

        save_data(
            df,
            PROCESSED_DATA
        )

        print("=" * 60)
        print("PREPROCESSING COMPLETED SUCCESSFULLY!")
        print("=" * 60)

        logging.info(
            "✅ Phase 4D Execution Complete!"
        )

    except Exception as error:

        logging.error(
            f"Pipeline execution failed: {str(error)}"
        )


# ============================================================
# Program Entry Point
# ============================================================

if __name__ == "__main__":
    main()