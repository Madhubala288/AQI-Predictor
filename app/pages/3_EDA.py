import streamlit as st
import pandas as pd
from pathlib import Path


st.set_page_config(
    page_title="AQI EDA",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_data.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

if not DATA_FILE.exists():

    st.error(
        "Processed dataset not found."
    )

    st.stop()


df = pd.read_csv(
    DATA_FILE
)


if "Timestamp" in df.columns:

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "📊 Exploratory Data Analysis"
)

st.caption(
    "Historical air-quality and weather data analysis."
)


st.info(
    "📍 Karachi historical dataset"
)


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.subheader(
    "📋 Dataset Overview"
)

missing_values = int(
    df.isna().sum().sum()
)

duplicates = int(
    df.duplicated().sum()
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Rows",
        len(df)
    )

with c2:

    st.metric(
        "Columns",
        len(df.columns)
    )

with c3:

    st.metric(
        "Missing Values",
        missing_values
    )

with c4:

    st.metric(
        "Duplicates",
        duplicates
    )


st.divider()


# ============================================================
# AQI DISTRIBUTION
# ============================================================

if "AQI" in df.columns:

    st.subheader(
        "🌍 AQI Distribution"
    )

    st.bar_chart(
        df["AQI"]
        .value_counts()
        .sort_index(),
        height=350
    )

    st.divider()


# ============================================================
# TEMPERATURE
# ============================================================

if "Temperature" in df.columns:

    st.subheader(
        "🌡️ Temperature Distribution"
    )

    st.line_chart(
        df[
            ["Temperature"]
        ],
        height=350
    )

    st.divider()


# ============================================================
# HUMIDITY
# ============================================================

if "Humidity" in df.columns:

    st.subheader(
        "💧 Humidity"
    )

    st.line_chart(
        df[
            ["Humidity"]
        ],
        height=350
    )

    st.divider()


# ============================================================
# POLLUTANTS
# ============================================================

pollutants = [
    "PM2.5",
    "PM10",
    "CO",
    "NO2",
    "SO2",
    "O3",
    "NH3"
]

available_pollutants = [
    column
    for column in pollutants
    if column in df.columns
]

if available_pollutants:

    st.subheader(
        "🧪 Pollutant Concentrations"
    )

    st.line_chart(
        df[
            available_pollutants
        ],
        height=450
    )

    st.divider()


# ============================================================
# CORRELATION
# ============================================================

numeric_df = (
    df
    .select_dtypes(
        include="number"
    )
)

if not numeric_df.empty:

    st.subheader(
        "🔗 Correlation Matrix"
    )

    correlation = (
        numeric_df
        .corr()
        .round(2)
    )

    st.dataframe(
        correlation,
        width="stretch"
    )

    st.divider()


# ============================================================
# TIME SERIES
# ============================================================

if (
    "Timestamp" in df.columns
    and "AQI" in df.columns
):

    st.subheader(
        "🕒 AQI Time Series"
    )

    time_series = (
        df
        .dropna(
            subset=[
                "Timestamp"
            ]
        )
        .sort_values("Timestamp")
        .set_index("Timestamp")[
            ["AQI"]
        ]
    )

    st.line_chart(
        time_series,
        height=400
    )

    st.divider()


# ============================================================
# DATA PREVIEW
# ============================================================

st.subheader(
    "🔍 Dataset Preview"
)

st.dataframe(
    df.head(100),
    width="stretch",
    hide_index=True
)