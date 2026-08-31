import streamlit as st
import pandas as pd
from pathlib import Path

from utils import get_aqi_category


st.set_page_config(
    page_title="AQI Forecast",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PREDICTION_FILE = (
    BASE_DIR
    / "predictions"
    / "predictions.csv"
)


# ============================================================
# LOAD
# ============================================================

if not PREDICTION_FILE.exists():

    st.error("Prediction file not found.")
    st.stop()


df = pd.read_csv(
    PREDICTION_FILE
)

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

df["Predicted_AQI"] = pd.to_numeric(
    df["Predicted_AQI"],
    errors="coerce"
)

df = (
    df
    .dropna(
        subset=[
            "Timestamp",
            "Predicted_AQI"
        ]
    )
    .sort_values("Timestamp")
    .reset_index(drop=True)
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "📈 AQI Forecast"
)

st.caption(
    "Detailed machine-learning forecast for Karachi."
)


st.info(
    "📍 Karachi | 72-hour forecasting system"
)


# ============================================================
# DAILY SUMMARY
# ============================================================

st.subheader(
    "📅 Daily Forecast Summary"
)

forecast_df = df.copy()

forecast_df["Date"] = (
    forecast_df["Timestamp"]
    .dt.date
)

daily_summary = (
    forecast_df
    .groupby("Date")["Predicted_AQI"]
    .agg(
        Average_AQI="mean",
        Minimum_AQI="min",
        Maximum_AQI="max"
    )
    .reset_index()
)

for column in [
    "Average_AQI",
    "Minimum_AQI",
    "Maximum_AQI"
]:

    daily_summary[column] = (
        daily_summary[column]
        .round(2)
    )


st.dataframe(
    daily_summary,
    width="stretch",
    hide_index=True
)


st.divider()


# ============================================================
# DAILY TREND
# ============================================================

st.subheader(
    "📊 Daily AQI Trend"
)

daily_chart = (
    daily_summary
    .set_index("Date")[
        [
            "Average_AQI",
            "Minimum_AQI",
            "Maximum_AQI"
        ]
    ]
)

st.line_chart(
    daily_chart,
    height=400
)


st.divider()


# ============================================================
# HOURLY FORECAST
# ============================================================

st.subheader(
    "🕒 Hourly AQI Forecast"
)

hourly_display = df[
    [
        "Timestamp",
        "Predicted_AQI"
    ]
].copy()

hourly_display["Category"] = (
    hourly_display["Predicted_AQI"]
    .apply(get_aqi_category)
)

hourly_display["Predicted_AQI"] = (
    hourly_display["Predicted_AQI"]
    .round(3)
)

st.dataframe(
    hourly_display,
    width="stretch",
    hide_index=True
)


st.divider()


# ============================================================
# DOWNLOAD
# ============================================================

csv_data = (
    hourly_display
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    "⬇️ Download Forecast",
    csv_data,
    "karachi_aqi_forecast.csv",
    "text/csv"
)